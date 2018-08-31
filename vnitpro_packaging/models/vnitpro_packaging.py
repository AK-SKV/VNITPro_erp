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


class Packaging(models.Model):
    _name = 'vnitpro.packaging'
    _rec_name = 'name'

    name = fields.Char('Name', size=200, required=True)
    activate = fields.Selection([('not_used', 'Not used'), ('usage', 'Usage')],
                                'Status', required=True, default='usage')
    description = fields.Text('Description', size=900, track_visibility="onchange")
