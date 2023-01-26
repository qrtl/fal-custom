from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self):
        self.ensure_one()
        if self.env.context.get("proforma") or self.state not in ("sale", "done"):
            return self.env.ref(
                "sale_order_mail_template_with_subject.mail_template_send_quo_with_subject",
                raise_if_not_found=False,
            )
        else:
            return self._get_confirmation_template()

    def _get_confirmation_template(self):
        """Get the mail template sent on SO confirmation (or for confirmed SO's).

        :return: `mail.template` record or None if default template wasn't found
        """
        return self.env.ref(
            "sale_order_mail_template_with_subject.mail_template_send_confirmation_with_subject",
            raise_if_not_found=False,
        )

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals["subject"] = self.subject
        return invoice_vals

    subject = fields.Char(tracking=True)
