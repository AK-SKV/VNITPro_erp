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


class ContractConfigure(models.Model):
    _name = 'vnitpro.contract.configure'

    name = fields.Char('Contract Name', size=200, required=True)
    sign_day = fields.Date('Sign Day', required=True)
    customer = fields.Char('Customer', size=200, required=True)
    description = fields.Text('Description', size=900, track_visibility="onchange")
