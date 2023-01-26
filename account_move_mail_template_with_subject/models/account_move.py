from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
            "account_move_mail_template_with_subject.email_template_edi_credit_note_with_subject"
            if all(move.move_type == "out_refund" for move in self)
            else "account_move_mail_template_with_subject.email_template_send_invoice_with_subject"
        )

    subject = fields.Char(tracking=True)
