from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
            "account_move_mail_template_with_subject.email_template_credit_note"
            if all(move.move_type == "out_refund" for move in self)
            else "account_move_mail_template_with_subject.email_template_send_invoice"
        )

    subject = fields.Char(tracking=True)
