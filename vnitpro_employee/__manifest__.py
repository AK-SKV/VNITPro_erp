# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

{
    'name': 'Employee',
    'description': 'Manage Employee, Department',
    'summary': 'Employee Management',
    'category': 'Employee',
    'sequence': 2,
    'version': '1.0.0',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['vnitpro_base'],
    'demo': [
        'demo/department_demo.xml',
        'demo/position_demo.xml',
        'demo/res_partner_demo.xml',
        'demo/res_user_demo.xml',
        'demo/employee_demo.xml',
    ],
    'data': [
        'views/department_view.xml',
        'views/employee_view.xml',
        'views/position_view.xml',
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'menu/employees_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
