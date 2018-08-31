# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Product',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Consumption',
    "sequence": 2,
    'summary': 'Product',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base',
                'vnitpro_product_group'],
    'data': [
        'views/vnitpro_product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
