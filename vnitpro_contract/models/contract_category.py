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
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


# # author: Tu Vo, model: .py, model contract_category
# # tác giả: Võ Tuấn Tú, model: contract_category.py, model hạng mục hợp đồng

class ContractCategory(models.Model):
    _name = 'vnitpro.contract.category'

    # contract category information
    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')
    category = fields.Char('Category', required=True, track_visibility='onchange')
    facility_id = fields.Many2one('vnitpro.facility', 'Facility', required=True, track_visibility='onchange',
                                  domain="[('activate','=','usage')]")
    origin = fields.Char('Origin', track_visibility='onchange')
    quantity = fields.Float('Quantity', digits=(3, 2), required=True, track_visibility='onchange')
    unit = fields.Char('Unit', required=True, track_visibility='onchange')
    unit_price = fields.Float('Unit Price', digits=(3, 2), required=True, track_visibility='onchange')
    currency_id = fields.Many2one('vnitpro.currency', required=True, track_visibility='onchange',
                                  domain="[('activate','=','usage')]")
    cost_before_vat = fields.Float('Price Before VAT', compute='compute_cost', digits=(3, 2),
                                   track_visibility='onchange', store=True)
    vat = fields.Selection([(0, '0 %'), (5, '5 %'), (10, '10 %')], 'VAT %', required=True, default=0,
                           track_visibility='onchange')
    vat_cost = fields.Float('VAT Cost', digits=(3, 2), compute='compute_cost', readonly=True, store=True)
    cost_after_vat = fields.Float('Price After VAT', digits=(3, 2), compute='compute_cost', readonly=True, store=True)
    warranty_period = fields.Integer('Warranty Period(month)', required=True, track_visibility='onchange')
    warranty_start_date = fields.Date('Warranty Start Date', track_visibility='onchange')
    warranty_end_date = fields.Date('Warranty End Date', compute='compute_end_date', store=True,
                                    track_visibility='onchange')
    note = fields.Text('Note', track_visibility='onchange')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'contract_category_id', 'Attach File')

    # @api.model
    # def create(self, vals):
    #     record = super(ContractCategory, self).create(vals)
    #     contract_category_ids = self.search([('contract_id', '=', vals['contract_id'])])
    #     for contract_category in contract_category_ids:
    #         contract_category.write({'warranty_period': vals['warranty_period'],
    #                                  'warranty_start_date': vals['warranty_start_date'], })
    #     return record

    # @api.model
    # def write(self, vals):
    #     record = super(ContractCategory, self).write(vals)
    #     contract_category_ids = self.search([('contract_id', '=', self.contract_id.id), ('id', '!=', self.id)])
    #     _logger.warning(contract_category_ids)
    #     for contract_category in contract_category_ids:
    #         if 'warranty_period' in vals:
    #             warranty_period = vals['warranty_period']
    #             contract_category.write({'warranty_period': warranty_period})
    #         elif 'warranty_start_date' in vals:
    #             warranty_start_date = vals['warranty_start_date']
    #             contract_category.write({'warranty_start_date': warranty_start_date})
    #     return record

    # @api.model
    # def default_get(self, fields):
    #     defaults = super(ContractCategory, self).default_get(fields)
    #     last_ids = self.search([], order='id desc', limit=1)
    #     if last_ids:
    #         last_id = last_ids[0]
    #         defaults['facility_id'] = last_id.facility_id.id
    #         defaults['origin'] = last_id.origin
    #         defaults['warranty_period'] = last_id.warranty_period
    #         defaults['warranty_start_date'] = last_id.warranty_start_date
    #     return defaults

    @api.one
    @api.depends('quantity', 'unit_price', 'vat')
    def compute_cost(self):
        self.cost_before_vat = self.quantity * self.unit_price
        self.vat_cost = self.cost_before_vat * self.vat / 100
        self.cost_after_vat = self.vat_cost + self.cost_before_vat

    @api.one
    @api.depends('warranty_period', 'warranty_start_date')
    def compute_end_date(self):
        if self.warranty_start_date and self.warranty_period > 0:
            start_date = datetime.datetime.strptime(self.warranty_start_date, '%Y-%m-%d')
            end_date = start_date + relativedelta(months=+self.warranty_period)
            self.warranty_end_date = end_date

    @api.multi
    @api.onchange('quantity', 'unit_price', 'warranty_period')
    def change_category(self):
        for record in self:
            if record.quantity < 0:
                record.quantity = 0
            elif record.unit_price < 0:
                record.unit_price = 0
            elif record.warranty_period < 0:
                record.warranty_period = 0
            elif record.warranty_period > 1200:
                record.warranty_period = 1200

    @api.multi
    @api.constrains('quantity', 'unit_price', 'warranty_period', 'warranty_start_date', 'contract_id')
    def constrains_category(self):
        for record in self:
            if record.quantity == 0:
                raise ValidationError(_("Quantity have to be higher than 0!"))
            elif record.unit_price == 0:
                raise ValidationError(_("Unit price have to be higher than 0!"))
            elif record.warranty_period == 0:
                raise ValidationError(_("Warranty period have to be higher than 0!"))
            elif record.warranty_start_date and record.contract_id.contract_date and record.warranty_start_date < record.contract_id.contract_date:
                raise ValidationError(_("Warranty start date have to start after contract start date!"))
