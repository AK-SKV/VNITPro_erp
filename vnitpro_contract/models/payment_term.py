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


# # author: Tu Vo, model: .py, model payment_term
# # tác giả: Võ Tuấn Tú, model: payment_term.py, model điều khoản thanh toán

class PaymentTerm(models.Model):
    _name = 'vnitpro.payment.term'

    # payment term information
    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')
    payment_name = fields.Char('Payment Name', required=True, track_visibility='onchange')
    payment_price = fields.Float('Payment Price', required=True, digits=(3, 2), track_visibility='onchange')
    start_date = fields.Date('Start Date', track_visibility='onchange')
    end_date = fields.Date('End Date', track_visibility='onchange')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'payment_term_id', 'Attach File')

    @api.multi
    @api.constrains('quantity', 'unit_price', 'start_date', 'end_date', 'contract_id')
    def constrains_term(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Start date have to start before end date!"))
            elif record.payment_price == 0:
                raise ValidationError(_("Payment price have to be higher than 0!"))

    @api.multi
    @api.onchange('price')
    def change_payment_term(self):
        for record in self:
            if record.price < 0:
                record.price = 0
