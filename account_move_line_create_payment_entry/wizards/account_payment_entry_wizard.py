# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, _, fields, models


class AccountPaymentEntryWizard(models.TransientModel):
    _name = "account.payment.entry.wizard"
    _description = "Payment Entry Wizard"

    account_id = fields.Many2one(
        "account.account",
        string="Credit Account",
        required=True,
        domain="[('deprecated', '=', False)]",
        help="Select the account to be used as the credit or debit account for "
        "the total balance of the selected journal items.",
    )
    date = fields.Date(
        string="Accounting Date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    move_line_ids = fields.Many2many(
        "account.move.line", string="Move Lines", readonly=True
    )

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
        line_vals.append(
            Command.create({"account_id": self.account_id.id, "balance": balance})
        )
        entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": self.date,
                "line_ids": line_vals,
            }
        )
        entry.action_post()
        move_line_ids = self.move_line_ids | entry.line_ids.filtered(
            lambda x: x.account_id.id != self.account_id.id
        )
        move_line_ids.reconcile()
        return {
            "name": _("Journal Entry"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": entry.id,
            "target": "current",
        }
