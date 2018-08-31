# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Asset type',
    'description': 'vnitpro_asset_type',
    'summary': 'vnitpro_asset_type',
    'category': 'Website',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'data': [
        'views/vnitpro_asset_type_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/asset_type_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
