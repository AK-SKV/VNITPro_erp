# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Created by: tam.pt
###############################################################################

from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)


class BaseAttachment(models.Model):
    _inherit = 'vnitpro.base.attachment'

    contract_id = fields.Many2one('vnitpro.contract', 'Attachment')
    acceptance_payment_id = fields.Many2one('vnitpro.acceptance.payment', 'Attachment')
    asset_increase_id = fields.Many2one('vnitpro.asset.increase', 'Attachment')
    contract_sub_id = fields.Many2one('vnitpro.contract.sub', 'Attachment')
    contract_category_id = fields.Many2one('vnitpro.contract.category', 'Attachment')
    guarantee_contract_id = fields.Many2one('vnitpro.guarantee.contract', 'Attachment')
    liquidation_id = fields.Many2one('vnitpro.contract', 'Attachment')
    payment_term_id = fields.Many2one('vnitpro.payment.term', 'Attachment')
