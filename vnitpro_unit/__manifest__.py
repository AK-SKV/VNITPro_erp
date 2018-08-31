# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

{
    'name': 'Unit',
    'description': 'Unit module in VNITPro ERP',
    'summary': 'Unit module',
    'category': 'unit',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/unit_view.xml',
        'security/ir.model.access.csv',
        'data/vnitpro_unit_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
