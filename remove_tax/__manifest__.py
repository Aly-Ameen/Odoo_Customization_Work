# estate/__manifest__.py
{
    'name': "remove_tax",
    'version': '1.0',
    'depends': ['sale','account', 'stock'],
    'author': "Aly Ameen" & "Muhammad Wael",
    'category': 'Remove Taxes from Sales Order and Invoices',
    'description': """
    Adding Price margin percentage in products
    """,
    
    'data': [
        "report/inherit_sale_order_remove_tax.xml",
        'views/inherit_product_template.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
