# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _convert(self, from_amount, to_currency, company, date, round=True):
        liquidity_amount_currency = self.env.context.get("liquidity_amount_currency")
        if liquidity_amount_currency:
            return liquidity_amount_currency
        return super()._convert(from_amount, to_currency, company, date, round)
