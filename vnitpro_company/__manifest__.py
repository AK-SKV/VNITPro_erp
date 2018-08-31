# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

{
    'name': 'Company',
    'description': 'Manage Company',
    'summary': 'Company Management',
    'category': 'Company',
    'sequence': 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/company_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
