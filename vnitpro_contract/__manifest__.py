# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
###############################################################################

{
    'name': 'Contract',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Contract',
    "sequence": 2,
    'summary': 'Manage Contract',
    'complexity': "easy",
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': [
        'vnitpro_base',
        'vnitpro_bidder',
        'vnitpro_contract_type',
        'vnitpro_payment_capital',
        'vnitpro_currency',
        'vnitpro_purpose_of_use',
        'vnitpro_contract_formality',
        'vnitpro_guarantee',
        'vnitpro_sub',
        'vnitpro_facility',
        'vnitpro_asset_type',
        'vnitpro_employee',
        'report_xlsx'
    ],
    'demo': [
        'demo/purpose_of_use_demo.xml',
        'demo/contract_1_demo.xml',
        'demo/contract_2_demo.xml',
    ],
    'data': [
        'data/data_view.xml',
        'views/contract_view.xml',
        'views/guarantee_contract_view.xml',
        'views/payment_term_view.xml',
        'views/contract_sub_view.xml',
        'views/asset_increase_view.xml',
        'views/acceptance_payment_view.xml',
        'views/contract_category_view.xml',
        'views/liquidation_view.xml',
        'views/contract_dashboard_view.xml',
        'views/recent_access.xml',
        'views/vnitpro_contract_assets.xml',
        'wizard/gen_contract_list_report_view.xml',
        'wizard/gen_contract_list_detail_report_view.xml',
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'reports/reports_menu.xml',
        'reports/report_contract_list_view.xml',
        'reports/report_contract_list_detail_view.xml',
        'menu/contract_menu.xml',
        'menu/contract_configure_menu.xml',
        'menu/vnitpro_contract_report_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
