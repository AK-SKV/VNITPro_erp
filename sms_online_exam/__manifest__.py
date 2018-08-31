# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


{
    'name': 'SMS Online Exam',
    'description': 'Manage Quiz And Manage Online Exam',
    'summary': 'Online Exam Module',
    'category': 'Quiz',
    "sequence": 10,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base', 'website', 'web'],
    'data': [
        # 'views/assets.xml',
        'views/contestant_view.xml',
        'views/object_view.xml',
        'views/process_view.xml',
        'views/question_view.xml',
        'views/exam_information_view.xml',
        'views/exam_result_view.xml',
        'menu/online_exam_menu.xml',
        'website/templates/online_exam_contest_page_template.xml',
        'website/templates/online_exam_done_page_template.xml',
        'website/templates/online_exam_register_page_template.xml',
        'website/exam_website.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
