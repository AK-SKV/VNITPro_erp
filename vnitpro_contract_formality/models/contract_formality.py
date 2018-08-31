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

# author: Tu Vo, model: contract_formality.py, module contract formality
# tác giả: Võ Tuấn Tú, model: contract_formality.py, module danh mục hình thức hợp đồng

class ContractFormality(models.Model):
    _name = 'vnitpro.contract.formality'
    _inherit = 'vnitpro.base.information'