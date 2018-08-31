# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re, logging

_logger = logging.getLogger(__name__)

# author: Tu Vo, model: guarantee.py, module guarantee configure
# tác giả: Võ Tuấn Tú, model: guarantee.py, module danh mục bảo lãnh

class Guarantee(models.Model):
    _name = 'vnitpro.guarantee'
    _inherit = 'vnitpro.base.information'
