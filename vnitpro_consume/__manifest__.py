# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Consume Management',
    'description': 'Consume Management',
    'summary': 'Consume Management',
    'category': 'Consume',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base',
                'vnitpro_customer',
                'vnitpro_unit',
                'vnitpro_currency',
                'vnitpro_taxes',
                'vnitpro_delivery_formality',
                'vnitpro_product',
                'vnitpro_product_group',
                'vnitpro_warehouse',
                'vnitpro_inventory',
                'vnitpro_packaging',
                'vnitpro_employee',
                'vnitpro_company',
                'vnitpro_contract_configure',
                'vnitpro_delivery_unit',
                'vnitpro_delivery_place',
                'vnitpro_inspection_unit'],
    'data': [
        'views/delivery_plan_view.xml',
        'views/order_view.xml',
        'views/tracking_card_view.xml',
        'views/vnitpro_inventory_export_product_view.xml',
        'views/vnitpro_direct_import_product_view.xml',
        'wizard/gen_consume_product_report_view.xml',
        'reports/report_consume_product_view.xml',
        'reports/reports_menu.xml',
        'menu/consume_root_menu.xml',
        'menu/consume_menu.xml',
        'menu/consume_configure_menu.xml',
        'menu/consume_report_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
