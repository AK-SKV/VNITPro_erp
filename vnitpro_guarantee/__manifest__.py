# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Guarantee',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Contract',
    "sequence": 2,
    'summary': 'Guarantee Configure',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'demo': [
        'demo/guarantee_demo.xml',
    ],
    'data': [
        'views/guarantee_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
