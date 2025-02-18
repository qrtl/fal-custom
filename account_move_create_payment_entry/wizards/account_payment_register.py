# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    payment_entry = fields.Boolean(
        help="Technical field to determine whether the wizard will "
        "act as a payment entry wizard."
    )

    def _create_payments(self):
        self.ensure_one()
        if self.payment_entry and self.group_payment:
            move_ids = self.env["account.move"].browse(
                self._context.get("active_ids", [])
            )
            remaining_amount = self.amount
            total_converted_amount = 0.0
            for move in move_ids:
                if remaining_amount <= 0:
                    break
                allocated_original = min(remaining_amount, move.amount_residual)
                conversion_rate = self.env["res.currency"]._get_conversion_rate(
                    move.currency_id,
                    self.company_id.currency_id,
                    self.company_id,
                    move.invoice_date,
                )
                allocated_converted = allocated_original * conversion_rate
                total_converted_amount += allocated_converted
                remaining_amount -= allocated_original
            if self.payment_type == "inbound":
                liquidity_amount_currency = total_converted_amount
            else:
                liquidity_amount_currency = -total_converted_amount
            self = self.with_context(
                liquidity_amount_currency=liquidity_amount_currency
            )
        return super(AccountPaymentRegister, self)._create_payments()

    def _reconcile_payments(self, to_process, edit_mode=False):
        if self.payment_entry and self.group_payment:
            return True
        return super()._reconcile_payments(to_process, edit_mode)
