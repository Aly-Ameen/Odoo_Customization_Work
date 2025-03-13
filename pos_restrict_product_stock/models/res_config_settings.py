from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Inherited res configuration setting for adding fields for
                restricting out-of-stock products"""
    _inherit = 'res.config.settings'

    is_display_stock = fields.Boolean(related="pos_config_id.is_display_stock",
                                      string="Display Stock in POS",
                                      readonly=False,
                                      help="Enable if you want to show the "
                                           "quantity of products.")
    is_restrict_product = fields.Boolean(
        related="pos_config_id.is_restrict_product",
        string="Restrict Product Out of Stock in POS", readonly=False,
        help="Enable if you want restrict of stock product from POS")
    stock_type = fields.Selection(related="pos_config_id.stock_type",
                                  string="Stock Type", readonly=False,
                                  help="In which quantity type you"
                                       "have to restrict and display in POS")
