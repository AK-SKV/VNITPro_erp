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


class Warehouse(models.Model):
    _name = 'vnitpro.warehouse'
    _inherit = 'vnitpro.base.information'

