# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_create_payment_entry(self):
        if len(set(self.mapped("partner_id.id"))) > 1:
            raise UserError(_("All selected records must have the same partner."))
        if len(set(self.mapped("move_type"))) > 1:
            raise UserError(_("All selected records must have the same move type."))
        return {
            "name": _("Create Payment Entry"),
            "type": "ir.actions.act_window",
            "res_model": "account.payment.entry.wizard",
            "view_mode": "form",
            "view_id": self.env.ref(
                "account_move_line_create_payment_entry.view_account_payment_entry_wizard_form"
            ).id,
            "target": "new",
            "context": {"default_move_line_ids": [(6, 0, self.ids)]},
        }
