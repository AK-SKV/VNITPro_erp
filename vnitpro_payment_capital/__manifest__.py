# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Payment capital',
    'description': 'vnitpro_payment_capital',
    'summary': 'vnitpro_payment_capital',
    'category': 'Website',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'demo': [
        'demo/payment_capital_demo.xml'
    ],
    'data': [
        'views/vnitpro_payment_capital_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
