# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    analytic_account_display_only_name = fields.Boolean(
        default=True,
        help="If enabled, the display name of analytic account will be shown "
        "only name.",
    )
