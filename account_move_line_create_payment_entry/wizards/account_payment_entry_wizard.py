# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, _, fields, models
from odoo.exceptions import UserError


class AccountPaymentEntryWizard(models.TransientModel):
    _name = "account.payment.entry.wizard"
    _description = "Payment Entry Wizard"

    partner_id = fields.Many2one("res.partner", required=True)
    journal_id = fields.Many2one(
        "account.journal",
        required=True,
        domain="[('type', '=', 'bank')]",
        help="Select the journal to be used as the journal for the entry.",
    )
    currency_id = fields.Many2one("res.currency", required=True)
    date = fields.Date(
        string="Payment Date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    move_line_ids = fields.Many2many(
        "account.move.line", string="Move Lines", readonly=True
    )

    def _get_payment_type(self):
        if self.move_line_ids[0].move_type in ["in_invoice", "out_refund"]:
            return "outbound"
        return "inbound"

    def _get_partner_type(self):
        if self.move_line_ids[0].account_id.account_type == "asset_receivable":
            return "customer"
        return "supplier"

    def create_payment_entry(self):
        self.ensure_one()
        line_vals = [
            Command.create(
                {
                    "account_id": rec.account_id.id,
                    "partner_id": rec.partner_id.id,
                    "amount_currency": -rec.amount_currency,
                    "currency_id": rec.currency_id.id,
                    "balance": -rec.balance,
                }
            )
            for rec in self.move_line_ids
        ]
        balance = sum(self.move_line_ids.mapped("balance"))
        amount_currency = sum(self.move_line_ids.mapped("amount_currency"))
        payment_type = self._get_payment_type()
        partner_type = self._get_partner_type()
        available_payment_method_lines = (
            self.journal_id._get_available_payment_method_lines(payment_type)
        )
        payment_method_line_id = available_payment_method_lines[0]._origin
        outstanding_account_id = False
        if payment_type == "inbound":
            outstanding_account_id = (
                payment_method_line_id.payment_account_id
                or self.journal_id.company_id.account_journal_payment_debit_account_id
            )
        else:
            outstanding_account_id = (
                payment_method_line_id.payment_account_id
                or self.journal_id.company_id.account_journal_payment_credit_account_id
            )
        if not outstanding_account_id:
            raise UserError(_("There is no outstanding account for the payment."))
        line_vals.append(
            Command.create(
                {
                    "account_id": outstanding_account_id.id,
                    "amount_currency": amount_currency,
                    "currency_id": self.currency_id.id,
                    "balance": balance,
                }
            )
        )
        entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": self.journal_id.id,
                "date": self.date,
                "line_ids": line_vals,
            }
        )
        payment_vals = {
            "move_id": entry.id,
            "date": self.date,
            "amount": abs(amount_currency),
            "payment_type": payment_type,
            "partner_type": partner_type,
            "journal_id": self.journal_id.id,
            "currency_id": self.currency_id.id,
            "partner_id": self.partner_id.id,
            "payment_method_line_id": payment_method_line_id.id,
            "destination_account_id": self.move_line_ids[0].account_id.id,
        }
        payment = (
            self.env["account.payment"]
            .with_context(
                create_payment_entry=True, skip_account_move_synchronization=True
            )
            .create(payment_vals)
        )
        payment.action_post()
        return {
            "name": _("Journal Entry"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": entry.id,
            "target": "current",
        }
