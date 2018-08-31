# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Currency',
    'description': 'Currency module',
    'summary': 'Currency module in VNITPro ERP',
    'category': 'currency',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/currency_view.xml',
        'security/ir.model.access.csv',
        'data/currency_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
