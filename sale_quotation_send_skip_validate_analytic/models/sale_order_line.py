# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _validate_analytic_distribution(self):
        if self.env.context.get("skip_validate_analytic"):
            return
        super()._validate_analytic_distribution()
