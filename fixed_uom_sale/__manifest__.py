# -*- coding: utf-8 -*-
{
    'name': "Fixed Unit of Measure for Sales",

    'summary': """Fixed Unit of Measure for Sales""",

    'description': """
        Fixed Unit of Measure for Sales
    """,

    'author': "Yahia Saleh",
    'website': "yahiasaleh911@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '19.6',

    # any module necessary for this one to work correctly
    'depends': ['sale_advanced', 'purchase', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        # 'views/product_packaging_report_views.xml',
        'views/sale_order_views.xml'
    ]
}
