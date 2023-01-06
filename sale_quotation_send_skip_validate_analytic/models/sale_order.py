# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_send(self):
        return super(
            SaleOrder, self.with_context(skip_validate_analytic=True)
        ).action_quotation_send()
