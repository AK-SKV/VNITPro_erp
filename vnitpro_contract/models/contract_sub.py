# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


# # author: Tu Vo, model: .py, model contract_sub
# # tác giả: Võ Tuấn Tú, model: contract_sub.py, model phụ lục hợp đồng

class ContractSub(models.Model):
    _name = 'vnitpro.contract.sub'

    # contract sub information
    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')
    sub_code = fields.Char('Sub Code', required=True, track_visibility='onchange')
    sub_type = fields.Many2one('vnitpro.sub', 'Sub Type', required=True, track_visibility='onchange',
                               domain="[('activate','=','usage')]")
    price_before_vat = fields.Float('Price Before VAT', digits=(3, 2), track_visibility='onchange')
    vat = fields.Selection([(0, '0 %'), (5, '5 %'), (10, '10 %')], 'VAT %', default=0, track_visibility='onchange')
    price_after_vat = fields.Float('Price Sub', compute='compute_price', digits=(3, 0), track_visibility='onchange')
    created_date = fields.Date('Created Date', track_visibility='onchange')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'contract_sub_id', 'Attach File')

    _sql_constraints = [
        ('unique_sub_code', 'unique(sub_code,contract_id)', 'The sub code already exists, please try another.')]

    @api.multi
    @api.onchange('sub_code')
    def change_sub_code(self):
        for record in self:
            if record.sub_code:
                sub_code = record.sub_code
                record.sub_code = sub_code.upper()

    @api.one
    @api.depends('price_before_vat', 'vat')
    def compute_price(self):
        vat_cost = self.price_before_vat * self.vat / 100
        self.price_after_vat = vat_cost + self.price_before_vat

    @api.multi
    @api.onchange('price_before_vat')
    def change_sub(self):
        for record in self:
            if record.price_before_vat < 0:
                record.price_before_vat = 0
