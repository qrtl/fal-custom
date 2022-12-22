# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _validate_analytic_distribution(self):
        if not self.env.context.get("skip_validate_analytic"):
            for line in self.filtered(
                lambda l: not l.display_type and l.state in ["draft", "sent"]
            ):
                line._validate_distribution(
                    **{
                        "product": line.product_id.id,
                        "business_domain": "sale_order",
                        "company_id": line.company_id.id,
                    }
                )
