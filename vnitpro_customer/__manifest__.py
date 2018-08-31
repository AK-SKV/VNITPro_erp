# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Customer',
    'description': 'Customer',
    'summary': 'Customer',
    'category': 'Consume',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/vnitpro_customer_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
