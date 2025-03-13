from odoo import fields, models


class PosConfig(models.Model):
    """Inherited pos configuration setting for adding some
            fields for restricting out-of stock"""
    _inherit = 'pos.config'

    is_display_stock = fields.Boolean(string="Display Stock in POS",
                                      help="Enable if you want to show "
                                           "quantity of products")
    is_restrict_product = fields.Boolean(
        string="Restrict Product Out-of Stock in POS",
        help="Enable if you want restrict of stock product from pos")
    stock_type = fields.Selection([('qty_on_hand', 'Qty on Hand'),
                                   ('virtual_qty', 'Virtual Qty'),
                                   ('both', 'Both')], required=True,
                                  default='qty_on_hand', string="Stock Type",
                                  help="In which quantity type you"
                                       " have to restrict and display")
