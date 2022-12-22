# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_send(self):
        """Override of quotation send to skip checking analytic distribute
        when quotation is sent.
        Opens a wizard to compose an email, with relevant mail template loaded by default"""
        self.ensure_one()
        self.order_line.with_context(
            skip_validate_analytic=True
        )._validate_analytic_distribution()
        lang = self.env.context.get("lang")
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        mail_layout = "mail.mail_notification_layout_with_responsible_signature"
        ctx = {
            "default_model": "sale.order",
            "default_res_id": self.id,
            "default_use_template": bool(mail_template),
            "default_template_id": mail_template.id if mail_template else None,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "default_email_layout_xmlid": mail_layout,
            "proforma": self.env.context.get("proforma", False),
            "force_email": True,
            "model_description": self.with_context(lang=lang).type_name,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
