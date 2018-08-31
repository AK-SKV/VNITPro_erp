# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

LAND_TYPE = [
    ('1st_grade_house', '1st Grade House'),
    ('2nd_grade_house', '2nd Grade House'),
    ('3th_grade_house', '3th Grade House'),
    ('4th_grade_house', '4th Grade House'),
    ('apartment', 'Apartment'),
    ('villa', 'Villa'),
]

_logger = logging.getLogger(__name__)


class LandGroup(models.Model):
    _name = 'vnitpro.land.group'
    _inherit = 'vnitpro.base.information', 'mail.thread'
    _description = 'Land Group'

    land_type = fields.Selection(LAND_TYPE, 'Land Type', required=True, default="villa", track_visibility="onchange")
