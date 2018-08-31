# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################


{
    'name': 'Bidder',
    'description': 'Bidder module',
    'summary': 'Bidder in VNITPro ERP',
    'category': 'VNITPro ERP',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base', 'vnitpro_bank'],
    'demo': [
        'demo/bidder_demo.xml',
    ],
    'data': [
        'views/bidder_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
