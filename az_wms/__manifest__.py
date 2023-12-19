# -*- coding: utf-8 -*-
{
    'name': "WHM",

    'summary': """
               Warehouse Management System
""",

    'description': """
        Warehouse Management System
    """,

    'author': "Muhammad Bilal",
    'website': "https://www.alifzero.com",

    'category': 'stock',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','stock','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/seq.xml',
        'views/res_partner_views.xml',
        'views/product_template.xml',
        'views/stock_location_view.xml',
        'views/product_catgory_view.xml',
        'views/mill.xml',
        'views/sale_invoice.xml',
        'views/sale_return.xml',
        'views/res_config_setting_view.xml',
        'views/menu.xml',
    ],
}
