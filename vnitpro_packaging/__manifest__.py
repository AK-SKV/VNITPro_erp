# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Packaging',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Consumption',
    "sequence": 2,
    'summary': 'Packaging',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/vnitpro_packaging_view.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'auto_install': False,
}
