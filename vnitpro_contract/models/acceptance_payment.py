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


# # author: Tu Vo, model: .py, model acceptance_payment
# # tác giả: Võ Tuấn Tú, model: acceptance_payment.py, model tăng tài sản

class ContractSub(models.Model):
    _name = 'vnitpro.acceptance.payment'

    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')

    # Acceptance information
    acceptance_document_number = fields.Char('Acceptance Document Number', required=True, track_visibility='onchange')
    acceptance_document_name = fields.Char('Acceptance Document Name', required=True, track_visibility='onchange')
    acceptance_price_before_vat = fields.Float('Acceptance Price Before VAT', digits=(3, 2), required=True,
                                               track_visibility='onchange')
    vat = fields.Selection([(0, '0 %'),
                            (5, '5 %'),
                            (10, '10 %')], 'VAT %', required=True, default=0, track_visibility='onchange')
    acceptance_vat = fields.Float('Acceptance VAT', digits=(3, 2), compute='compute_acceptance', readonly=True,
                                  store=True)
    acceptance_price_after_vat = fields.Float('Acceptance Price After VAT', compute='compute_acceptance',
                                              store=True, digits=(3, 2), readonly=True, track_visibility='onchange')
    acceptance_date = fields.Datetime('Acceptance Date', required=True, track_visibility='onchange')
    acceptance_prefect_a = fields.Char('Acceptance Prefect A', track_visibility='onchange')
    acceptance_member_a = fields.Text('Acceptance Members A', track_visibility='onchange')
    acceptance_prefect_b = fields.Char('Acceptance Prefect B', track_visibility='onchange')
    acceptance_member_b = fields.Text('Acceptance Members B', track_visibility='onchange')
    acceptance_information = fields.Text('Acceptance Information', track_visibility='onchange')

    _sql_constraints = [('unique_number', 'unique(acceptance_document_number,contract_id)',
                         'The acceptance document number already exists, please try another.')]

    @api.multi
    @api.onchange('acceptance_document_number')
    def change_acceptance_document_number(self):
        for record in self:
            if record.acceptance_document_number:
                acceptance_document_number = record.acceptance_document_number
                record.acceptance_document_number = acceptance_document_number.upper()

    @api.one
    @api.depends('acceptance_price_before_vat', 'vat')
    def compute_acceptance(self):
        self.acceptance_vat = self.acceptance_price_before_vat * self.vat / 100
        self.acceptance_price_after_vat = self.acceptance_vat + self.acceptance_price_before_vat

    @api.multi
    @api.onchange('acceptance_document_number')
    def change_acceptance(self):
        for record in self:
            if record.acceptance_document_number:
                acceptance_document_number = record.acceptance_document_number
                record.acceptance_document_number = acceptance_document_number.upper()

    @api.multi
    @api.onchange('acceptance_price_before_vat')
    def change_acceptance(self):
        for record in self:
            if record.acceptance_price_before_vat < 0:
                record.acceptance_price_before_vat = 0

    @api.multi
    @api.constrains('acceptance_date', 'contract_id')
    def constrains_acceptance(self):
        for record in self:
            if record.acceptance_date and record.acceptance_date < record.contract_id.contract_date:
                raise ValidationError(_("Acceptance date have to start after contract start date!"))
            elif not re.match("^[a-zA-Z0-9_/\\\\]*$", record.acceptance_document_number):
                raise ValidationError(_(
                    "Invalid Code, please try again ( Acceptance document number only contains letters, numbers and character: / , \\ , _ )."))
            if record.acceptance_price_before_vat == 0:
                raise ValidationError(_("Acceptance price have to higher than 0!"))

    # Payment Information
    payment_number = fields.Char('Payment Number', required=True, track_visibility='onchange')
    payment_date = fields.Datetime('Payment Date', track_visibility='onchange')
    payment_price_before_vat = fields.Float('Payment Price Before VAT', digits=(3, 2), required=True,
                                            track_visibility='onchange')
    vat_2 = fields.Selection([(0, '0 %'),
                              (5, '5 %'),
                              (10, '10 %')], 'VAT %', required=True, default=0, track_visibility='onchange')
    payment_vat = fields.Float('Payment VAT', digits=(3, 2), compute='compute_payment', readonly=True, store=True)
    payment_price_after_vat = fields.Float('Payment Price After VAT', compute='compute_payment', digits=(3, 2),
                                           store=True, readonly=True, track_visibility='onchange')
    payment_capital = fields.Many2one('vnitpro.payment.capital', 'Payment Capital', track_visibility='onchange',
                                      domain="[('activate','=','usage')]")
    payment_employee = fields.Many2one('vnitpro.employee', 'Payment Employee', track_visibility='onchange',
                                       domain="[('activate','=','usage')]")
    payment_information = fields.Text('Payment Detail', track_visibility='onchange')

    @api.one
    @api.depends('payment_price_before_vat', 'vat_2')
    def compute_payment(self):
        self.payment_vat = self.payment_price_before_vat * self.vat_2 / 100
        self.payment_price_after_vat = self.payment_vat + self.payment_price_before_vat

    @api.multi
    @api.onchange('payment_number')
    def change_payment(self):
        for record in self:
            if record.payment_number:
                payment_number = record.payment_number
                record.payment_number = payment_number.upper()

    @api.multi
    @api.onchange('payment_price_before_vat')
    def change_payment_price(self):
        for record in self:
            if record.payment_price_before_vat < 0:
                record.payment_price_before_vat = 0

    @api.multi
    @api.constrains('payment_date', 'contract_id', 'payment_price_before_vat')
    def constrains_payment(self):
        for record in self:
            if record.payment_date and record.payment_date < record.contract_id.contract_date:
                raise ValidationError(_("Payment date have to start after contract start date!"))
            elif not re.match("^[a-zA-Z0-9_/\\\\]*$", record.payment_number):
                raise ValidationError(_(
                    "Invalid Code, please try again ( Payment number only contains letters, numbers and character: / , \\ , _ )."))
            elif record.payment_price_after_vat > record.contract_id.real_cost_after_vat:
                raise ValidationError(_("Payment price have to smaller than contract real cost!"))
            if record.payment_price_before_vat == 0:
                raise ValidationError(_("Payment price have to higher than 0!"))

    # Bill Information
    bill_price_before_vat = fields.Float('Bill Price Before VAT', digits=(3, 2), required=True,
                                         track_visibility='onchange')
    vat_3 = fields.Selection([(0, '0 %'),
                              (5, '5 %'),
                              (10, '10 %')], 'VAT %', required=True, default=0, track_visibility='onchange')
    bill_vat = fields.Float('Bill VAT', digits=(3, 2), compute='compute_bill', readonly=True)
    bill_price_after_vat = fields.Float('Bill Price After VAT', compute='compute_bill', digits=(3, 2),
                                        readonly=True, track_visibility='onchange')

    @api.one
    @api.depends('bill_price_before_vat', 'vat_3')
    def compute_bill(self):
        self.bill_vat = self.bill_price_before_vat * self.vat_3 / 100
        self.bill_price_after_vat = self.bill_vat + self.bill_price_before_vat

    @api.multi
    @api.onchange('bill_price_before_vat')
    def change_bill(self):
        for record in self:
            if record.bill_price_before_vat < 0:
                record.bill_price_before_vat = 0

    @api.multi
    @api.constrains('bill_price_before_vat')
    def constrains_bill(self):
        for record in self:
            if record.bill_price_before_vat == 0:
                raise ValidationError(_("Bill price have to higher than 0!"))

    # Warranty Guarantee Information
    guarantee_unit = fields.Char('Guarantee Unit', required=True, track_visibility='onchange')
    guarantee_start_date = fields.Date('Guarantee Start Date', track_visibility='onchange')
    guarantee_end_date = fields.Date('Guarantee End Date', tracl_visibility='onchange')
    guarantee_price = fields.Float('Guarantee Price', digits=(3, 2), track_visibility='onchange')

    @api.multi
    @api.constrains('guarantee_start_date', 'guarantee_end_date')
    def constrains_date(self):
        if self.guarantee_end_date < self.guarantee_start_date:
            raise ValidationError(_("Guarantee start date can't start after guarantee end date!"))

    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'acceptance_payment_id', 'Attach File')
