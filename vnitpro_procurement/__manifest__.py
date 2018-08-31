# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'Procurement',
    'description': 'vnitpro_procurement',
    'summary': 'procurement',
    'category': 'Website',
    "sequence": 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': [
        'vnitpro_base',
        'vnitpro_bidder',
        'vnitpro_payment_capital',
        'vnitpro_procurement_formality',
        'vnitpro_contract_type',
        'vnitpro_currency',
        'vnitpro_employee',
        'report_xlsx',
    ],
    'demo': [
        'demo/vnitpro_procurement_demo.xml',
        'demo/vnitpro_department_demo.xml',
    ],
    'data': [
        'views/vnitpro_procurement_sub_view.xml',
        'views/vnitpro_procurement_view.xml',
        'views/vnitpro_approve_pq_document_view.xml',
        'views/vnitpro_confirm_prequalification_view.xml',
        'views/vnitpro_bid_profile_view.xml',
        'views/vnitpro_ranking_list_view.xml',
        'views/vnitpro_negotiation_result_view.xml',
        'views/vnitpro_expertise_result_view.xml',
        'views/vnitpro_negotiation_result_view.xml',
        # 'views/vnitpro_processing_situation_view.xml',
        'views/vnitpro_procurement_dashboard_view.xml',
        'views/vnitpro_department_view.xml',
        'views/recent_access.xml',
        'views/vnitpro_procurement_assets.xml',
        'wizard/gen_procurement_list_report_view.xml',
        'wizard/gen_procurement_details_report_view.xml',
        'reports/reports_menu.xml',
        'reports/report_procurement_list_view.xml',
        'reports/report_procurement_details_view.xml',
        'security/security.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/vnitpro_procurement_dashboard_data.xml',
        'menu/vnitpro_procurement_menu.xml',
        'menu/vnitpro_procurement_configure_menu.xml',
        'menu/vnitpro_procurement_report_menu.xml',
        'demo/vnitpro_procurement_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
