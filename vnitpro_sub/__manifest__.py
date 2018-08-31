# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Sub',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Sub',
    "sequence": 2,
    'summary': 'Sub',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'demo': [
        'demo/sub_demo.xml'
    ],
    'data': [
        'views/sub_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
