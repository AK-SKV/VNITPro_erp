# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _name = 'vnitpro.company'
    _inherit = 'vnitpro.base.information'


    company_car_ids = fields.One2many('vnitpro.company.car', 'company_id', 'Company Car')
    company_romooc_ids = fields.One2many('vnitpro.company.romooc', 'company_id', 'Company Romooc')
