from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    batch_number = fields.Char(string="Batch Number", compute="_compute_batch_number")
    expiration_date = fields.Date(string="Expiration Date", compute="_compute_expiration_date")

    @api.depends("product_variant_ids")
    def _compute_batch_number(self):
        for product in self:
            # Find all lots for the product, ordered by expiration date (earliest first)
            lots = self.env["stock.lot"].search([
                ("product_id", "in", product.product_variant_ids.ids),
                ("expiration_date", "!=", False),  # Ensure expiration date exists
                ("product_qty", ">", 0)  # Ensure lot has available quantity
            ], order="expiration_date asc", limit=1)

            # Assign batch number based on the first valid lot
            product.batch_number = lots.name if lots else ""

    @api.depends("batch_number")
    def _compute_expiration_date(self):
        """Compute the expiration date based on the selected batch number."""
        for product in self:
            if product.batch_number:
                lot = self.env["stock.lot"].search([
                    ("name", "=", product.batch_number),
                    ("product_id", "in", product.product_variant_ids.ids)  # Ensure it's the correct product
                ], limit=1)
                product.expiration_date = lot.expiration_date if lot and lot.expiration_date else False
            else:
                product.expiration_date = False
