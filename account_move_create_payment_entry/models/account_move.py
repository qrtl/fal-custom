# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_create_payment_entry(self):
        if len(set(self.mapped("partner_id.id"))) > 1:
            raise UserError(_("All selected records must have the same partner."))
        if len(set(self.mapped("currency_id.id"))) > 1:
            raise UserError(_("All selected records must have the same currency."))
        if self[0].currency_id == self.env.company.currency_id:
            raise UserError(
                _(
                    "This action is used for moves that have a different currency "
                    "from the company currency."
                )
            )
        return {
            "name": _("Register Payment"),
            "res_model": "account.payment.register",
            "view_mode": "form",
            "context": {
                "active_model": "account.move",
                "active_ids": self.ids,
                "default_payment_entry": True,
                "default_group_payment": True,
            },
            "target": "new",
            "type": "ir.actions.act_window",
        }
