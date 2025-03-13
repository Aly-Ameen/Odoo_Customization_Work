{
    'name': 'Display Stock in POS | Restrict Out-of-Stock Products in POS',
    'version': '17.0.2.1.1',
    'category': 'Point of Sale',
    'summary': """Enhance your Point of Sale experience by preventing the 
    ordering of out-of-stock products during your session""",
    'description': """This module enables you to limit the ordering of 
     out-of-stock products in POS as well as display the available quantity for
      each product (on-hand quantity and virtual quantity).""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['point_of_sale'],
    'data': ['views/res_config_settings_views.xml'],
    'assets': {
        'point_of_sale._assets_pos': [
        '/pos_restrict_product_stock/static/src/js/RestrictStockPopup.js',
        '/pos_restrict_product_stock/static/src/js/ProductScreen.js',
        '/pos_restrict_product_stock/static/src/js/PaymentScreenPatch.js',
        '/pos_restrict_product_stock/static/src/js/OrderScreen.js',
        '/pos_restrict_product_stock/static/src/css/display_stock.css',
        '/pos_restrict_product_stock/static/src/xml/ProductItem.xml',
        '/pos_restrict_product_stock/static/src/xml/RestrictStockPopup.xml',],
},

    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
