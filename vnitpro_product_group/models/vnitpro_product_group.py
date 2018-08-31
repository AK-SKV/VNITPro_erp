# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re, logging

_logger = logging.getLogger(__name__)


class ProductGroup(models.Model):
    _name = 'vnitpro.product.group'
    _inherit = 'vnitpro.base.information'

    unit_id = fields.Many2one('vnitpro.unit', 'Unit', required=True)
    # unit_id = fields.Char( 'Unit', required=True)

