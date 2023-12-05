from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_mail_template(self):
        template_name = super(AccountMove, self)._get_mail_template()
        template = self.env.ref(template_name)
        for move in self:
            if move.move_type == "out_refund":
                template.write(
                    {
                        "subject": "{{object.subject or 'n/a'}}-クレジットノート送付(Ref {{object.name}})"
                    }
                )
                return template_name
            else:
                template.write(
                    {
                        "subject": "{{object.subject or 'n/a'}} - ご請求書の送付 (Ref {{object.name}})"
                    }
                )
                return template_name
