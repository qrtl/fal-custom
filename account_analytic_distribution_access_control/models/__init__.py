from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_analytic_accounting_user = fields.Boolean(
        string="Analytic Accounting User", implied_group="analytic.group_analytic_user"
    )
