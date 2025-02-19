# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    payment_entry = fields.Boolean(
        help="Technical field to determine whether the wizard will "
        "act as a payment entry wizard."
    )

    @api.depends("line_ids")
    def _compute_from_lines(self):
        super()._compute_from_lines()
        if self.payment_entry:
            self.can_edit_wizard = False
        return

    def _post_payments(self, to_process, edit_mode=False):
        if self.payment_entry:
            payments = self.env["account.payment"]
            for vals in to_process:
                payments |= vals["payment"]
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
                for rec in self.line_ids._origin
            ]
            balance = sum(self.line_ids.mapped("balance"))
            amount_currency = sum(self.line_ids.mapped("amount_currency"))
            line_vals.append(
                Command.create(
                    {
                        "account_id": payments.outstanding_account_id.id,
                        "amount_currency": amount_currency,
                        "currency_id": self.currency_id.id,
                        "balance": balance,
                    }
                )
            )
            entry = self.env["account.move"].create(
                {
                    "move_type": "entry",
                    "journal_id": payments.journal_id.id,
                    "date": self.payment_date,
                    "line_ids": line_vals,
                }
            )
            payments.move_id = entry.id
            # This is needed because when the journal entry is created after
            # the payment is created and linked, the journal_id field is shared
            # between both the payment and the entry. As a result, the computed
            # currency is triggered and assigned the company currency.
            payments.currency_id = self.currency_id.id
        return super()._post_payments(to_process, edit_mode)

    def _reconcile_payments(self, to_process, edit_mode=False):
        if self.payment_entry:
            return True
        return super()._reconcile_payments(to_process, edit_mode)

    def _create_payments(self):
        if self.payment_entry:
            self = self.with_context(skip_account_move_synchronization=True)
        return super(AccountPaymentRegister, self)._create_payments()
