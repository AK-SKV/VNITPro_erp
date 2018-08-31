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


# author: Tu Vo, model: procurement_formality.py, module procurement formality
# tác giả: Tú Võ, model: procurement_formality.py, module danh mục hình thức chọn thầu

class ProcurementFormality(models.Model):
    _name = 'vnitpro.procurement.formality'
    _inherit = 'vnitpro.base.information'
