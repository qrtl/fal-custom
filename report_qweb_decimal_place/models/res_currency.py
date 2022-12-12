# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    apply_price_unit_format = fields.Boolean()
