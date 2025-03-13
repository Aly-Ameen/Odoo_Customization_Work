from odoo import models, api, fields
from odoo.tools import float_compare

class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = "account.payment.register"

    @api.depends('line_ids')
    def _compute_amount(self):
        for wizard in self:
            if not wizard.line_ids:
                wizard.amount = 0.0
                continue

            # Get the related invoice (account.move)
            move = wizard.line_ids.mapped('move_id')
            if not move or not move.invoice_payment_term_id:
                wizard.amount = abs(sum(wizard.line_ids.mapped('amount_residual')))
                continue

            # Get total invoice amount
            total_invoice_amount = move.amount_total

            # Compute total amount already paid
            total_paid = total_invoice_amount - move.amount_residual

            # Compute remaining balance correctly
            remaining_balance = move.amount_residual

            # Prevent negative balances
            if remaining_balance <= 0:
                wizard.amount = 0.0
                continue

            # 🔹 Read the actual payment term dynamically
            payment_terms = move.invoice_payment_term_id.line_ids.sorted('nb_days')

            # Track all installments dynamically
            installments = []
            for term in payment_terms:
                if term.value == 'percent':
                    term_amount = total_invoice_amount * (term.value_amount / 100.0)
                else:  # Fixed amount case
                    term_amount = term.value_amount

                installments.append({
                    'term_amount': term_amount,
                    'paid': 0.0,  # This will store how much has been paid towards this installment
                    'remaining': term_amount  # Initially, the full installment is remaining
                })

            # Deduct already paid amounts from installments
            remaining_to_allocate = total_paid
            for installment in installments:
                if remaining_to_allocate > 0:
                    allocated = min(installment['remaining'], remaining_to_allocate)
                    installment['paid'] += allocated
                    installment['remaining'] -= allocated
                    remaining_to_allocate -= allocated

            # Find the next unpaid installment
            next_payment = None
            for installment in installments:
                if installment['remaining'] > 0:
                    next_payment = installment['remaining']
                    break  # Stop at the first unpaid installment

            # Apply the next installment payment amount
            wizard.amount = min(next_payment, remaining_balance) if next_payment else remaining_balance
