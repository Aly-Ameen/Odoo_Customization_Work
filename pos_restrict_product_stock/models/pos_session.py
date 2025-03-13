from odoo import models, api

class PosSession(models.Model):
    """Inherited POS session to load product quantity fields"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Load forecast and on-hand quantity fields into POS session."""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('qty_available')
        result['search_params']['fields'].append('virtual_available')
        return result

    @api.model
    def update_stock_after_order(self):
        """ Syncs stock from Inventory (`stock.quant`) to POS (`product.product`)."""
        products = self.env['product.product'].search([('available_in_pos', '=', True)])
        for product in products:
            stock_quant = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id', '=', self.config_id.stock_location_id.id)  # Ensure correct POS stock location
            ], limit=1)
            product.qty_available = stock_quant.quantity if stock_quant else 0

        return {'status': 'success', 'message': 'Stock updated in POS'}
