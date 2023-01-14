# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    solomon_tax_category = fields.Char(
        help="The set value will be used in Solomon data export.",
    )
    solomon_tax_id = fields.Char(
        help="The set value will be used in Solomon data export.",
    )
