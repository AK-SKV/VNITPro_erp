# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

{
    'name': 'Contract - Procurement Relation',
    'description': 'VNITPro Contract - Procurement',
    'summary': 'Manage Contract And Procurement Relation',
    'category': 'Relation',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': [
        'vnitpro_procurement',
        'vnitpro_contract',
    ],
    'data': [
        'views/vnitpro_contract_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
