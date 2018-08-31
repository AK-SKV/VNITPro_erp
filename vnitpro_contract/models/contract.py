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
import pytz
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


# # author: Tu Vo, model: contract.py, module contract
# # tác giả: Võ Tuấn Tú, model: contract.py, module quản lý hợp đồng

class Contract(models.Model):
    _name = 'vnitpro.contract'
    _inherit = 'vnitpro.base.information', 'mail.thread'
    _description = 'Contract'
    _order = 'create_date desc'

    # contract information
    contract_kind = fields.Selection([('output', 'Output Contract'),
                                      ('input', 'Input Contract')], 'Contract Kind', required=True,
                                     default='output', track_visibility='onchange')
    bidder_a = fields.Many2one("vnitpro.bidder", "Bidder A", required=True, track_visibility='onchange',
                               domain="[('id','!=',bidder_b),('activate','=','usage')]")
    bidder_b = fields.Many2one("vnitpro.bidder", "Bidder B", required=True, track_visibility='onchange',
                               domain="[('id','!=',bidder_a),('activate','=','usage')]")
    code = fields.Char('Contract Code', required=True, track_visibility='onchange')
    name = fields.Char('Contract Name', required=True, track_visibility='onchange')
    contract_type_id = fields.Many2one('vnitpro.contract.type', 'Contract Type', required=True,
                                       domain="[('activate','=','usage')]",
                                       track_visibility='onchange')
    contract_date = fields.Date('Contract Date', required=True, track_visibility='onchange')
    contract_creator = fields.Many2one('vnitpro.employee', 'Contract Creator',
                                       default=lambda self: self.get_creator(), readonly=True)
    contract_formality_id = fields.Many2one('vnitpro.contract.formality', 'Contract Formality', required=True,
                                            domain="[('activate','=','usage')]",
                                            track_visibility='onchange')
    guarantee = fields.Boolean('Guarantee', default=False, track_visibility='onchange')
    start_date = fields.Date('Contract Start Date', required=True, track_visibility='onchange')
    duration = fields.Integer('Duration', required=True, track_visibility='onchange')
    unit = fields.Selection([('day', 'Day'),
                             ('week', 'Week'),
                             ('month', 'Month'),
                             ('year', 'Year')],
                            required=True, default='day', track_visibility='onchange')
    package_price = fields.Float('Package Price', required=True, digits=(3, 2), track_visibility='onchange')
    adjusted_price = fields.Float('Adjusted Price', required=True, digits=(3, 2), track_visibility='onchange')
    permanent_price = fields.Float('Permanent Price', required=True, digits=(3, 2), track_visibility='onchange')
    vat = fields.Selection([('0', '0 %'),
                            ('5', '5 %'),
                            ('10', '10 %')],
                           'VAT %', required=True, default='0', track_visibility='onchange')
    cost_before_vat = fields.Float('Cost Before VAT', compute='compute_cost', digits=(3, 2), readonly=True,
                                   track_visibility='onchange')
    vat_cost = fields.Float('VAT Cost', digits=(3, 2), compute='compute_cost', readonly=True)
    cost_after_vat = fields.Float('Cost After VAT', digits=(3, 2), compute='compute_cost', readonly=True)
    currency = fields.Many2one('vnitpro.currency', 'Currency', required=True, track_visibility='onchange',
                               domain="[('activate','=','usage')]")
    funds = fields.Many2one('vnitpro.payment.capital', 'Funds', track_visibility='onchange',
                            domain="[('activate','=','usage')]")
    purpose_of_use = fields.Many2many('vnitpro.purpose.of.use', string='Purpose of Use',
                                      domain="[('activate','=','usage')]", track_visibility='onchange')
    real_cost_before_vat = fields.Float('Real Cost Before VAT', digits=(3, 2), required=True,
                                        track_visibility='onchange')
    real_cost_after_vat = fields.Float('Real Cost After VAT', digits=(3, 2), required=True, track_visibility='onchange')
    guarantee_unit = fields.Text('Guarantee Unit', track_visibility='onchange')
    guarantee_start_date = fields.Date('Guarantee Start Date', track_visibility='onchange')
    guarantee_end_date = fields.Date('Guarantee End Date', tracl_visibility='onchange')
    guarantee_price = fields.Float('Guarantee Price', digits=(3, 2), track_visibility='onchange')
    note = fields.Text('Note', track_visibility='onchange')
    status = fields.Selection([('pending', 'Pending'),
                               ('in_process', 'In Process'),
                               ('asset_increase', 'Asset Increase'),
                               ('acceptance_payment', 'Acceptance - Payment'),
                               ('liquidated_finalized', 'Liquidated - Finalized'),
                               ('on_hold', 'On Hold'),
                               ('cancel', 'Cancel')], 'Status', default='pending')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'contract_id', 'Attach File')
    state = fields.Text("State", compute='compute_state')
    expire_date = fields.Date(compute='compute_state', store=True)
    day_left = fields.Integer(compute='compute_state', store=True)
    contract_dashboard = fields.Many2one('vnitpro.contract.dashboard', 'Contract', compute='compute_dashboard',
                                         store=True)
    warning = fields.Selection([('guarantee_expire', 'Guarantee Expire'),
                                ('warranty_expire', 'Warranty Expire'),
                                ('guarantee_warranty_expire', 'Guarantee Warranty Expire')], 'Warning',
                               compute='compute_state', store=True)

    @api.multi
    @api.onchange('contract_kind')
    def get_default_bidder(self):
        bidder = self.env['vnitpro.bidder'].search([('code', '=', 'VNITPRO')], limit=1)
        if self.contract_kind == 'output':
            self.bidder_b = False
            self.bidder_a = bidder.id
        elif self.contract_kind == 'input':
            self.bidder_a = False
            self.bidder_b = bidder.id

    def get_creator(self):
        creator = self.env['vnitpro.employee'].search([('res_user_id', '=', self.env.user.id)], limit=1)
        if creator:
            return creator.id
        else:
            return False

    @api.one
    @api.depends('status')
    def compute_dashboard(self):
        contract_dashboard = self.env['vnitpro.contract.dashboard'].search([('status', '=', self.status)])[0]
        self.contract_dashboard = contract_dashboard.id

    # one2many to guarantee
    # bảng con bảo lãnh
    guarantee_ids = fields.One2many('vnitpro.guarantee.contract', 'contract_id', 'Guarantee Contract')

    # one2many to contract category
    # bảng con hạng mục hợp đồng
    contract_category_ids = fields.One2many('vnitpro.contract.category', 'contract_id', 'Contract Category')

    # one2many to payment_term
    # bảng con điều khoản thanh toán
    payment_term_ids = fields.One2many('vnitpro.payment.term', 'contract_id', 'Payment Term')

    # one2many to contract_sub
    # bảng con phụ lục hợp đồng
    contract_sub_ids = fields.One2many('vnitpro.contract.sub', 'contract_id', 'Contract Sub')

    # one2many to asset_increase
    # bảng con tăng tài sản
    asset_increase_ids = fields.One2many('vnitpro.asset.increase', 'contract_id', 'Asset Increase')

    # one2many to acceptance_payment
    # bảng con nghiệm thu - thanh toán
    acceptance_payment_ids = fields.One2many('vnitpro.acceptance.payment', 'contract_id', 'Acceptance Payment')

    @api.multi
    @api.onchange('duration')
    def change_duration(self):
        for record in self:
            if record.duration < 0:
                record.duration = 0
            else:
                if record.unit == 'day':
                    if record.duration > 36525:
                        record.duration = 36525
                elif record.unit == 'week':
                    if record.duration > 5217:
                        record.duration = 5217
                elif record.unit == 'month':
                    if record.duration > 1200:
                        record.duration = 1200
                elif record.unit == 'year':
                    if record.duration > 100:
                        record.duration = 100

    @api.multi
    @api.onchange('package_price', 'adjusted_price', 'permanent_price', 'real_cost_before_vat', 'real_cost_after_vat',
                  'guarantee_price')
    def change_price(self):
        for record in self:
            if record.package_price < 0:
                record.package_price = 0
            elif record.adjusted_price < 0:
                record.adjusted_price = 0
            elif record.permanent_price < 0:
                record.permanent_price = 0
            elif record.real_cost_before_vat < 0:
                record.real_cost_before_vat = 0
            elif record.real_cost_after_vat < 0:
                record.real_cost_after_vat = 0
            elif record.guarantee_price < 0:
                record.guarantee_price = 0

    @api.multi
    @api.depends('start_date', 'duration', 'guarantee_end_date', 'contract_category_ids')
    def compute_state(self):
        for record in self:
            state = ''
            date = datetime.datetime.today()
            tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
            tz_database = pytz.timezone('UTC')
            date = tz_database.localize(date)
            date = date.astimezone(tz_current)
            date = date.date()
            if record.status == 'in_process':
                if record.start_date and record.duration:
                    start_date = datetime.datetime.strptime(record.start_date, '%Y-%m-%d')
                    if record.unit == 'day':
                        end_date = start_date + relativedelta(days=+record.duration)
                    elif record.unit == 'week':
                        end_date = start_date + relativedelta(weeks=+record.duration)
                    elif record.unit == 'month':
                        end_date = start_date + relativedelta(months=+record.duration)
                    elif record.unit == 'year':
                        end_date = start_date + relativedelta(years=+record.duration)
                    record.expire_date = end_date
                    day = (end_date.date() - date).days
                    if day < 0:
                        state += _('- Contract out of date: %d day(s) \n') % abs(day)
                    elif day == 0:
                        state += _('- Contract expired today \n')
                    elif abs(day) < 15:
                        record.day_left = 1
                        state += _('- Contract %d day(s) left \n') % abs(day)
            if len(record.contract_category_ids) > 0:
                day = 15
                for contract_category_id in record.contract_category_ids:
                    if contract_category_id.warranty_end_date:
                        warranty_end_date = datetime.datetime.strptime(contract_category_id.warranty_end_date,
                                                                       '%Y-%m-%d')
                        warranty_day = (warranty_end_date.date() - date).days
                        if warranty_day < day:
                            day = warranty_day
                if 0 <= day < 15:
                    state += _('- Warranty expire in %d day(s) \n') % abs(day)
                    record.warning = 'guarantee_warranty_expire'
            if record.guarantee_end_date:
                guarantee_end_date = datetime.datetime.strptime(record.guarantee_end_date, '%Y-%m-%d')
                day = (guarantee_end_date.date() - date).days
                if 0 <= day < 15:
                    state += _('- Guarantee contract expire in %d day(s) \n') % abs(day)
                    record.warning = 'guarantee_expire'
            if len(record.acceptance_payment_ids) > 0:
                day = 15
                for acceptance_payment_id in record.acceptance_payment_ids:
                    if acceptance_payment_id.guarantee_end_date:
                        guarantee_end_date = datetime.datetime.strptime(acceptance_payment_id.guarantee_end_date,
                                                                        '%Y-%m-%d')
                        guarantee_day = (guarantee_end_date.date() - date).days
                        if guarantee_day < day:
                            day = guarantee_day
                if 0 <= day < 15:
                    state += _('- Guarantee warranty expire in %d day(s) \n') % abs(day)
                    record.warning = 'warranty_expire'
            record.state = state

    @api.one
    @api.depends('package_price', 'adjusted_price', 'permanent_price', 'vat')
    def compute_cost(self):
        self.cost_before_vat = self.package_price + self.adjusted_price + self.permanent_price
        self.vat_cost = self.cost_before_vat * int(self.vat) / 100
        self.cost_after_vat = self.vat_cost + self.cost_before_vat

    @api.multi
    @api.constrains('package_price', 'adjusted_price', 'permanent_price', 'start_date', 'contract_date',
                    'guarantee_start_date', 'guarantee_end_date', 'guarantee_price', 'duration')
    def constrains_contract(self):
        for record in self:
            if record.package_price == 0 and record.adjusted_price == 0 and record.permanent_price == 0:
                raise ValidationError(_("One of three category price have to be more than 0!"))
            elif record.start_date and record.contract_date and record.start_date < record.contract_date:
                raise ValidationError(_("Contract start date can start before contract date!"))
            elif record.guarantee_start_date and record.guarantee_end_date and record.guarantee_start_date > record.guarantee_end_date:
                raise ValidationError(_("Guarantee end date can start before guarantee start date!"))
            elif record.duration == 0:
                raise ValidationError(_("Duration have to higher than 0!"))

    @api.multi
    def cancel(self):
        self.status = 'cancel'

    @api.multi
    def on_hold(self):
        self.status = 'on_hold'

    @api.multi
    def process(self):
        self.status = 'in_process'

    @api.multi
    def asset_increase(self):
        if len(self.asset_increase_ids) > 0:
            self.status = 'asset_increase'
        else:
            raise ValidationError(_("You have to add an asset increase before asset increase confirm!"))

    @api.multi
    def acceptance_payment(self):
        if len(self.acceptance_payment_ids) > 0:
            self.status = 'acceptance_payment'
        else:
            raise ValidationError(_("You have to add an acceptance payment before acceptance payment confirm!"))
