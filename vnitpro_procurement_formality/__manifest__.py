# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Procurement Formality',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Procurement',
    "sequence": 2,
    'summary': 'Procurement Formality',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'demo': [
        'demo/procurement_formality_demo.xml',
    ],
    'data': [
        'views/procurement_formality_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
