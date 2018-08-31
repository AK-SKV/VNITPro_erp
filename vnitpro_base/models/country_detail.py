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
import locale
import logging
_logger = logging.getLogger(__name__)


class ResCity(models.Model):
    _name = 'vnitpro.res.city'
    _inherit = 'vnitpro.base.information'

    name = fields.Char(translate=True)
    phone_code = fields.Char('Phone Code', size=50)
    country_id = fields.Many2one('res.country', 'Country', required=True)


class ResDistrict(models.Model):
    _name = 'vnitpro.res.district'
    _inherit = 'vnitpro.base.information'

    name = fields.Char(translate=True)
    city_id = fields.Many2one('vnitpro.res.city', 'City', required=True)


class ResWard(models.Model):
    _name = 'vnitpro.res.ward'
    _inherit = 'vnitpro.base.information'

    name = fields.Char(translate=True)
    district_id = fields.Many2one('vnitpro.res.district', 'District', required=True)
