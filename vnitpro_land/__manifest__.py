# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

{
    'name': 'Land',
    'description': 'Manage about land type, land group, land use rights',
    'summary': 'Manage Land Use Rights',
    'category': 'Lands Of Use',
    "sequence": 10,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base', 'vnitpro_purpose_of_use', 'report_xlsx', 'base', 'mail'],
    'demo': [
        'demo/purpose_of_use_demo.xml',
    ],
    'data': [
        'data/hbt_company.xml',
        'views/assess_category_view.xml',
        'views/assess_status_view.xml',
        'views/process_unit_view.xml',
        'views/land_group_view.xml',
        'views/land_use_rights_view.xml',
        'views/assets.xml',
        'views/purpose_of_use_view.xml',
        'views/owner_information_view.xml',
        'views/extra_owner_information_view.xml',
        'views/usage_origin_view.xml',
        'views/usage_duration_view.xml',
        'security/land_security.xml',
        'security/ir.model.access.csv',
        'wizard/gen_villa_list_report_view.xml',
        'report/report.xml',
        'report/villa_list_report_view.xml',
        'menu/land_menu.xml',
        'menu/purpose_of_use_menu.xml',
        'menu/report_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
