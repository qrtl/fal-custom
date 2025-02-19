# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        self.ensure_one()
        if self.env.context.get("create_payment_entry"):
            return []
        return super()._prepare_move_line_default_vals(write_off_line_vals)
