# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY VNITPro(<http://vnitpro.vn>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'VNITPro Support',
    'category': 'Planner',
    'summary': 'Help to configure',
    'version': '11.0.1.0.0',
    'license': 'LGPL-3',
    "sequence": 3,
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['base', 'web_settings_dashboard'],
    'data': [
        'views/rework_system_view.xml',
    ],
    'qweb': ['static/src/xml/change_menu.xml'],
    'installable': True,
    'auto_install': False,
}
