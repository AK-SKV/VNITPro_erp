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


# author: Tu Vo, model: sub.py, module sub
# tác giả: Tú Võ, model: sub.py, module danh mục loại phụ lục

class Sub(models.Model):
    _name = 'vnitpro.sub'
    _inherit = 'vnitpro.base.information'
