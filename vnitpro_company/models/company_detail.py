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


class CompanyCar(models.Model):
    _name = 'vnitpro.company.car'
    _rec_name = "car_number"

    company_id = fields.Many2one('vnitpro.company', 'Company', required=True, ondelete='cascade')
    car_number = fields.Char('Car Number')


class CompanyRomooc(models.Model):
    _name = 'vnitpro.company.romooc'
    _rec_name = "romooc_number"


    company_id = fields.Many2one('vnitpro.company', 'Company', required=True, ondelete='cascade')
    romooc_number = fields.Char('Romooc Number')
