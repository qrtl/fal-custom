from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self):
        template_name = super(SaleOrder, self)._find_mail_template()
        if self.env.context.get("proforma") or self.state not in ("sale", "done"):
            template_name.write(
                {
                    "subject": "{{object.subject or 'n/a'}} - お見積りの送付 (Ref {{object.name}})"
                }
            )
            return template_name
        else:
            template_name.write(
                {
                    "subject": "{{object.subject or 'n/a'}} - 注文確認書の送付 (Ref {{object.name}})"
                }
            )
            return template_name
