# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Base-VNITPro',
    'description': 'Base module',
    'summary': 'Base module in VNITPro ERP',
    'category': 'base',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['base', 'mail', 'board', 'rowno_in_tree', 'vietnam_translate', 'backend_theme_v11'],
    'demo': [
        'demo/mail_server_demo.xml',
        'demo/company_demo.xml',
    ],
    'data': [
        'demo/update_lang.xml',
        'demo/root_demo.xml',
        'views/asset_view.xml',
        'views/vnitpro_template.xml',
        'security/security.xml',
        'report/report_template.xml',
        'menu/base_menu.xml',
        'menu/system_sequence_menu.xml',
        'data/vietnam_city_data_vn.xml',
        'data/vietnam_district_data_vn.xml',
        'data/vietnam_ward_data_vn.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
