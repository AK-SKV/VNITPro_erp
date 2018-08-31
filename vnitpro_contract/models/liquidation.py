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


# # author: Tu Vo, model: .py, model liquidation
# # tác giả: Võ Tuấn Tú, model: liquidation.py, model thanh lý

class Liquidation(models.Model):
    _inherit = 'vnitpro.contract'

    # liquidation information
    information = fields.Text('Liquidation Information', track_visibility='onchange')
    liquidation_number = fields.Char('Liquidation Number', track_visibility='onchange')
    liquidation_date = fields.Datetime('Liquidation Date', track_visibiliy='onchange')
    total_contract_price = fields.Float('Total Contract Price', digits=(3, 2), compute='compute_total_price',
                                        store=True, track_visibility='onchange', readonly=True)
    currency_liquidation = fields.Many2one('vnitpro.currency', 'Currency', compute='compute_currency',
                                           readonly=True, store=True)
    total_paid_contract_price = fields.Float('Total Paid Contract Price', digits=(3, 2), compute='compute_paid_price',
                                             track_visibility='onchange', readonly=True, store=True)
    remain_contract_price = fields.Float('Remain Contract Price', digits=(3, 2), compute='compute_remain_price',
                                         track_visibility='onchange', readonly=True, store=True)
    file_attachment_liquidation_ids = fields.One2many('vnitpro.base.attachment', 'liquidation_id', 'Attach File')

    @api.multi
    @api.depends('currency')
    def compute_currency(self):
        for record in self:
            record.currency_liquidation = record.currency

    @api.multi
    @api.depends('real_cost_after_vat')
    def compute_total_price(self):
        for record in self:
            record.total_contract_price = record.real_cost_after_vat

    @api.multi
    @api.depends('acceptance_payment_ids')
    def compute_paid_price(self):
        for record in self:
            for val in record.acceptance_payment_ids:
                record.total_paid_contract_price += val.payment_price_after_vat

    @api.multi
    @api.depends('total_contract_price', 'total_paid_contract_price')
    def compute_remain_price(self):
        for record in self:
            record.remain_contract_price = record.total_contract_price - record.total_paid_contract_price

    @api.multi
    @api.constrains('liquidation_date', 'contract_date', 'liquidation_number', 'remain_contract_price')
    def constrains_liquidation(self):
        for record in self:
            if record.liquidation_date and record.liquidation_date < record.contract_date:
                raise ValidationError(_("Liquidation date have to start after contract start date!"))
            elif record.liquidation_number and not re.match("^[a-zA-Z0-9_/\\\\]*$", record.liquidation_number):
                raise ValidationError(_(
                    "Invalid Code, please try again (Liquidation number only contains numbers and character: / , \\ , _ )."))
            elif record.remain_contract_price < 0:
                raise ValidationError(_("Total pay contract price have to smaller than contract cost!"))

    @api.multi
    def edit_liquidation(self):
        liquidation_view = self.env.ref('vnitpro_contract.view_vnitpro_liquidation_form', False)
        return {
            'name': _('Liquidation'),
            'domain': [],
            'res_model': 'vnitpro.contract',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'target': 'new',
            'views': [(liquidation_view.id, 'form')],
            'view_id': liquidation_view.id,
        }

    @api.multi
    def delete_liquidation(self):
        self.information = False
        self.liquidation_number = False
        self.liquidation_date = False
        self.total_contract_price = False
        self.currency_liquidation = False
        self.total_paid_contract_price = False
        self.remain_contract_price = False

    @api.multi
    def save_refresh(self):
        return True

    @api.multi
    def liquidated_finalized(self):
        if self.information and self.liquidation_number and self.liquidation_date:
            self.status = 'liquidated_finalized'
        else:
            raise ValidationError(
                _("You have to fill all the liquidation finalized information before liquidation finalized confirm!"))
