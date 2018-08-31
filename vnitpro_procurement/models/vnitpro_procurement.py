# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
import datetime
import pytz
import logging
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


ARENA = [('inland', 'Inland'), ('International', 'International')]
PROCUREMENT_TYPE = [('1', 'Provide Non-Consulting Services'),
                    ('2', 'Composite'),
                    ('3', 'Merchandise Shoping'),
                    ('4', 'Selective﻿ Advisory'),
                    ('5', 'Build')]

PROCUREMENT_METHOD = [('1', 'Two Packpage'),
                      ('2', 'One Packpage'),
                      ('3', 'Following The Shortened Procedure')]

CONTRACT_DURATION = [('1', 'By start date, end date'),
                     ('2', 'By date'),
                     ('3', 'By week'),
                     ('4', 'By month'),
                     ('5', 'By quarter'),
                     ('6', 'By year')]

TYPE_CONTRACT = [('1', 'By Fixed Price'), ('2', 'By Adjusted Value'),
                 ('3', 'By Time'), ('4', 'By Package')]
STATUS_EXPIRE = [('out_of_date', 'Out Of Date'),
                 ('unexpired', 'Unexpired'),
                 ('expire_today', 'Expire Today')]


class Procurement(models.Model):
    _name = "vnitpro.procurement"
    _inherit = "vnitpro.base.information", "mail.thread"
    _order = 'create_date desc'
    _description = "Procurement"

    arena = fields.Selection(ARENA, 'Arena', required=True, default="inland")
    vat_information = fields.Float('VAT Information', required=True, track_visibility="onchange", digits=(3, 2))
    procurement_type = fields.Selection(PROCUREMENT_TYPE, 'Procurement type', required=True)
    procurement_formality_id = fields.Many2one('vnitpro.procurement.formality', 'Procurement Selection Form',
                                               required=True, domain="[('activate','=', 'usage')]")
    procurement_method = fields.Selection(PROCUREMENT_METHOD, 'Procurement Method', required=True)
    from_date = fields.Date('From date', required=True, track_visibility="onchange")
    to_date = fields.Date('To date', required=True, track_visibility="onchange")
    type_of_contract = fields.Selection(TYPE_CONTRACT, 'Type Of Contract', required=True)
    funds = fields.Many2many('vnitpro.payment.capital', string='Funds', domain="[('activate','=', 'usage')]",
                             track_visibility="onchange")
    procurement_information_attachment_ids = fields.One2many('vnitpro.base.attachment', 'procurement_information_id',
                                                             'Attach Files')
    # contract_duration
    contract_duration = fields.Selection(CONTRACT_DURATION, required=True, default='1')
    start_date = fields.Date('Start date', required=True, track_visibility="onchange", default=fields.Date.today())
    end_date = fields.Date('End date', track_visibility="onchange")
    days = fields.Integer('Days', size=10, track_visibility="onchange")
    weeks = fields.Integer('Weeks', size=4, track_visibility="onchange")
    months = fields.Integer('Months', size=3, track_visibility="onchange")
    quarters = fields.Integer('Quarters', size=3, track_visibility="onchange")
    years = fields.Integer('Years', size=2, track_visibility="onchange")
    expire_date = fields.Date('Expire Date', compute='compute_expire_date', store=True)

    @api.one
    @api.depends('contract_duration', 'start_date', 'end_date', 'days', 'weeks', 'months', 'quarters', 'years')
    def compute_expire_date(self):
        if self.contract_duration:
            if self.contract_duration == '1' and self.end_date:
                self.expire_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
            elif self.start_date:
                duration = relativedelta(days=+0)
                if self.contract_duration == '2' and self.days:
                    duration = relativedelta(days=+self.days)
                elif self.contract_duration == '3' and self.weeks:
                    duration = relativedelta(weeks=+self.weeks)
                elif self.contract_duration == '4' and self.months:
                    duration = relativedelta(months=+self.months)
                elif self.contract_duration == '5' and self.quarters:
                    duration = relativedelta(months=+(self.quarters * 3))
                elif self.contract_duration == '6' and self.years:
                    duration = relativedelta(years=+self.years)
                self.expire_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') + duration

    @api.one
    @api.constrains('vat_information')
    def validate_vat_information(self):
        _logger.warning(datetime.datetime.now())
        if self.vat_information and self.vat_information <= 0:
            raise ValidationError(_('Vat Information must be bigger than 0 !'))

    @api.one
    @api.constrains('from_date', 'to_date')
    def validate_from_date_to_date(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError(_('To Date cannot be set before From Date !'))

    @api.one
    @api.constrains('start_date', 'end_date', 'days', 'weeks', 'months', 'quarters', 'years')
    def validate_contract_duration(self):
        if self.contract_duration == '1' and self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(_('End Date cannot be set before Start Date !'))
            elif self.start_date < self.to_date:
                raise ValidationError(_('Start Date cannot be set before To Date !'))
        elif self.contract_duration == '2' and self.days <= 0:
            raise ValidationError(_('Days must be bigger than 0'))
        elif self.contract_duration == '3' and self.weeks <= 0:
            raise ValidationError(_('Weaks must be bigger than 0'))
        elif self.contract_duration == '4' and self.months <= 0:
            raise ValidationError(_('Months must be bigger than 0'))
        elif self.contract_duration == '5' and self.quarters <= 0:
            raise ValidationError(_('Quaters must be bigger than 0'))
        elif self.contract_duration == '6' and self.years <= 0:
            raise ValidationError(_('Years must be bigger than 0'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    procurement_information_id = fields.Many2one(
        'vnitpro.procurement', 'Procurement Information', ondelete="cascade")
