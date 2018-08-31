# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Project',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Project',
    "sequence": 2,
    'summary': 'Manage Project',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_bidder',
                'vnitpro_payment_capital',
                'vnitpro_base',
                'vnitpro_currency'],
    'data': [
        'views/project_view.xml',
        'views/project_dashboard_view.xml',
        'views/recent_access.xml',
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/project_dashboard_data.xml',
        'menu/project_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
