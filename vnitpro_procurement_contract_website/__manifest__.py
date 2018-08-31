# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY VNITPro(<http://vnitpro.vn>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Procurement Contract Website',
    'description': 'Beautifies Website',
    'category': 'Website',
    "sequence": 3,
    'version': '11.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'VNITPro',
    'website': 'http://vnitpro.vn',
    'depends': ['website', 'web'],
    'data': [
        'views/homepage.xml',
        'views/navbar_template.xml',
        'views/assets.xml',
        'views/footer_template.xml',
        'views/title_template.xml',
        'security/website_security.xml',
    ],
    'qweb': ['static/src/xml/add_guide.xml'],
}
