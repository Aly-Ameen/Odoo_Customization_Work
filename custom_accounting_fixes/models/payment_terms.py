from odoo import models, fields, api

from odoo.tools import float_compare


class PaymentTermsDetails(models.Model):
    _inherit = 'account.move'
    _description = 'handling the payment errors'


@api.depends('amount_residual', 'move_type', 'state', 'company_id', 'invoice_payment_term_id')
def _compute_payment_state(self):
    for invoice in self:
        if invoice.payment_state == 'invoicing_legacy':
            continue

        if invoice.state != 'posted' or not invoice.is_invoice(True):
            invoice.payment_state = 'not_paid'
            continue

        # Fetch payment terms
        payment_terms = invoice.invoice_payment_term_id._compute_terms(
            date_ref=invoice.invoice_date or invoice.date,
            currency=invoice.currency_id,
            company=invoice.company_id,
            tax_amount=invoice.amount_tax_signed,
            tax_amount_currency=invoice.amount_tax,
            untaxed_amount=invoice.amount_untaxed_signed,
            untaxed_amount_currency=invoice.amount_untaxed,
            sign=1 if invoice.is_inbound(include_receipts=True) else -1
        )

        # Calculate total payments made
        total_paid = sum(invoice.line_ids.mapped('matched_credit_ids.credit_move_id.amount_total'))
        total_due = sum(term['foreign_amount'] for term in payment_terms['line_ids'])

        if float_compare(total_paid, total_due, precision_rounding=invoice.currency_id.rounding) >= 0:
            invoice.payment_state = 'paid'
        elif total_paid > 0:
            invoice.payment_state = 'partial'
        else:
            invoice.payment_state = 'not_paid'
