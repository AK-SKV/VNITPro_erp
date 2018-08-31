# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################


{
    'name': 'Test',
    'description': 'Test module',
    'summary': 'Test in VNITPro ERP',
    'category': 'VNITPro ERP',
    "sequence": 0,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/test_view.xml',
        'views/nested_view.xml',
        'menu/test_menu.xml',
        'security/test_security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'security/permission_rules.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
