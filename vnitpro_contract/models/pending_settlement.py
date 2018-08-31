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


# # author: Tu Vo, model: .py, model pending_settlement
# # tác giả: Võ Tuấn Tú, model: pending_settlement.py, model chờ quyết toán

class PendingSettlement(models.Model):
    _inherit = 'vnitpro.contract'

    settlement_file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'pending_settlement_id', 'Attach File')
