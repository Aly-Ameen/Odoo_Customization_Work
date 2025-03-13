from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self, soft=True):
        """
        Override _post to enforce that the invoice date cannot be before the lock date.
        If it is, raise an error to force the user to change it.
        """
        for move in self:
            # Retrieve the lock date from company settings (choose tax_lock_date or fiscalyear_lock_date)
            lock_date = move.company_id.tax_lock_date or move.company_id.fiscalyear_lock_date
            if lock_date and move.invoice_date and move.invoice_date < lock_date:
                raise UserError(_(
                    "The Invoice Date (%s) is before the lock date (%s). "
                    "Please change the Invoice Date to a valid date before posting."
                ) % (move.invoice_date, lock_date))
        # Call the base _post() to proceed with posting
        return super(AccountMove, self)._post(soft=soft)
