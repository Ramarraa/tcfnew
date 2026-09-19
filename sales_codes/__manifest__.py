# -*- coding: utf-8 -*-
{
    'name': 'Sales Codes',
    'version': '19.0.0.1',
    'summary': '',
    'author': 'kHALIL AL SHAREEF',
    'description': """
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/product_customer_info_view.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_move_line_views.xml',
    ],
    'depends': [
        'sale_management',
        'stock',
        'sale_stock',
    ],
}


