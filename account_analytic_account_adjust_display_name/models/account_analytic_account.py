# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def name_get(self):
        if not self.env.company.analytic_account_display_only_name:
            return super().name_get()
        res = []
        for analytic in self:
            res.append((analytic.id, analytic.name))
        return res
