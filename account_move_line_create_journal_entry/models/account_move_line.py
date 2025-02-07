# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_create_journal_entry(self):
        if len(set(self.mapped("partner_id.id"))) > 1:
            raise UserError(_("All selected records must have the same partner."))
        if any(line.move_id.move_type != "in_invoice" for line in self):
            raise UserError(_("All selected records must belong to vendor bills."))
        line_vals = []
        for rec in self:
            line_vals.append(
                (
                    0,
                    0,
                    {
                        "account_id": rec.account_id.id,
                        "partner_id": rec.partner_id.id,
                        "amount_currency": -rec.amount_currency,
                        "currency_id": rec.currency_id.id,
                        "balance": -rec.balance,
                    },
                )
            )
        balance = sum(self.mapped("balance"))
        credit_account = self.env.company.account_journal_payment_credit_account_id
        if not credit_account:
            raise UserError(
                _(
                    "There is no default credit account set up in the company. "
                    "Please configure it."
                )
            )
        line_vals.append((0, 0, {"account_id": credit_account.id, "balance": balance}))
        entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "line_ids": line_vals,
            }
        )
        return {
            "name": _("Journal Entry"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": entry.id,
            "target": "current",
        }
