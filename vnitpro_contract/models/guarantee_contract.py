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
import datetime

_logger = logging.getLogger(__name__)


# # author: Tu Vo, model: .py, model guarantee_contract
# # tác giả: Võ Tuấn Tú, model: guarantee_contract.py, model bảo lãnh

class GuaranteeContract(models.Model):
    _name = 'vnitpro.guarantee.contract'

    # guarantee information
    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')
    guarantee_type = fields.Many2one('vnitpro.guarantee', 'Guarantee Type', required=True, track_visibility='onchange',
                                     domain="[('activate','=','usage')]")
    guarantee_unit = fields.Char('Guarantee Unit', required=True, track_visibility='onchange')
    price = fields.Float('Price', required=True, digits=(3, 2), track_visibility='onchange')
    start_date = fields.Date('Start Date', required=True, track_visibility='onchange')
    end_date = fields.Date('End Date', required=True, track_visibility='onchange')
    note = fields.Text('Note', track_visibility='onchange')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'guarantee_contract_id', 'Attach File')
    status = fields.Selection([(1, 'Effect'), (2, 'Expired')], 'Status', compute='compute_status', required=True)

    @api.multi
    @api.depends('end_date')
    def compute_status(self):
        date = datetime.datetime.today()
        for record in self:
            if record.end_date:
                end_date = datetime.datetime.strptime(record.end_date, '%Y-%m-%d')
                if date > end_date:
                    record.status = 2
                else:
                    record.status = 1

    @api.multi
    @api.constrains('start_date', 'end_date', 'price')
    def constrains(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Guarantee contract end date can start before guarantee contract start date!"))
            elif record.price == 0:
                raise ValidationError(_("Price have to higher than 0!"))

    @api.multi
    @api.onchange('price')
    def change_guarantee(self):
        for record in self:
            if record.price < 0:
                record.price = 0
