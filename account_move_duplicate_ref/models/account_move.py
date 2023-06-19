from odoo import _, api, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "ref" not in default:
            default["ref"] = _("%s (copy)", self.ref)
        return super(AccountMove, self).copy(default=default)
