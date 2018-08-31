# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Inventory',
    'description': 'Inventory',
    'summary': 'Inventory',
    'category': 'Consume',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base',
                'vnitpro_unit',
                'vnitpro_product',
                'vnitpro_product_group',
                'vnitpro_company',
                'vnitpro_warehouse',
                'vnitpro_packaging'
                ],
    'data': [
        'views/vnitpro_inventory_import_product_view.xml',
        'views/vnitpro_inventory_export_product_view.xml',
        'views/vnitpro_inventory_import_packaging_view.xml',
        'views/vnitpro_inventory_export_packaging_view.xml',
        'views/vnitpro_inventory_import_formality_standard_view.xml',
        'views/vnitpro_inventory_import_formality_defects_view.xml',
        'views/vnitpro_inventory_export_formality_view.xml',
        'wizard/gen_import_product_report_view.xml',
        'reports/report_import_product_view.xml',
        'reports/reports_menu.xml',
        'menu/vnitpro_inventory_menu.xml',
        'menu/vnitpro_inventory_configure_menu.xml',
        'menu/vnitpro_inventory_report_menu.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
