# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging
from odoo.addons.vnitpro_base.models.base import BaseInformation as base

_logger = logging.getLogger(__name__)


class DeliveryPlan(models.Model):
    _name = 'vnitpro.delivery.plan'
    _inherit = 'vnitpro.base.information'

    code = fields.Char('Plan Number', required=True, track_visibility='onchange')
    name = fields.Char('Plan Name', required=True, track_visibility='onchange')
    sign_date = fields.Date('Sign Date', required=True, track_visibility='onchange')
    month = fields.Selection([('jan', 'January'),
                              ('feb', 'February'),
                              ('mar', 'March'),
                              ('apr', 'April'),
                              ('may', 'May'),
                              ('jun', 'June'),
                              ('jul', 'July'),
                              ('aug', 'August'),
                              ('sep', 'September'),
                              ('oct', 'October'),
                              ('nov', 'November'),
                              ('dec', 'December'), ], 'Month', required=True, track_visibility='onchange')
    year = fields.Char('Year', required=True, default='2018', size=4, track_visibility='onchange')
    delivery_day = fields.Char('Delivery Day', compute='compute_day', store=True, track_visibility='onchange')
    product_information_ids = fields.One2many('vnitpro.product.information', 'delivery_plan_id', 'Product Information')

    @api.one
    @api.depends('month', 'year')
    def compute_day(self):
        if self.month == 'jan':
            month = _('January')
        elif self.month == 'feb':
            month = _('February')
        elif self.month == 'mar':
            month = _('March')
        elif self.month == 'apr':
            month = _('April')
        elif self.month == 'may':
            month = _('May')
        elif self.month == 'jun':
            month = _('June')
        elif self.month == 'jul':
            month = _('July')
        elif self.month == 'aug':
            month = _('August')
        elif self.month == 'sep':
            month = _('September')
        elif self.month == 'oct':
            month = _('October')
        elif self.month == 'nov':
            month = _('November')
        elif self.month == 'dec':
            month = _('December')
        self.delivery_day = month + '/' + self.year

    @api.one
    @api.constrains('year')
    def constrains_year(self):
        if self.year and not re.match("^[0-9]*$", self.year):
            raise ValidationError(_("Invalid year, please try again."))
        if len(self.product_information_ids) < 1:
            raise ValidationError(_("Empty product, please add product to plan!"))

    @api.multi
    @api.constrains('code')
    def _compute_special_character_code(self):
        for record in self:
            if not re.match("^[a-zA-Z0-9_\-/\\\\]*$", record.code):
                raise ValidationError(_(
                    "Invalid Code, please try again ( Code only contains letters, numbers and character: / , \\ , - _ ) ."))


class ProductInformation(models.Model):
    _name = 'vnitpro.product.information'
    _inherit = 'mail.thread'
    _rec_name = 'name'

    name = fields.Char('Name', compute='compute_name')
    delivery_plan_id = fields.Many2one('vnitpro.delivery.plan', 'Delivery Plan', required=True, ondelete='cascade')
    contract_id = fields.Many2one('vnitpro.contract.configure', 'By Contract', required=True)
    sign_day = fields.Date('Contract Sign Date', related='contract_id.sign_day', store=True, readonly=True)
    customer = fields.Char('Customer', related='contract_id.customer', store=True, readonly=True)
    product_group_id = fields.Many2one('vnitpro.product.group', 'Product', required=True)
    weight = fields.Float('Weight', required=True)
    unit_id = fields.Many2one('vnitpro.unit', related='product_group_id.unit_id', readonly=True)
    delivery_formality_id = fields.Many2one('vnitpro.delivery.formality', 'Delivery Formality', required=True)
    expected_price = fields.Float('Expected Price', required=True)
    currency_id = fields.Many2one('vnitpro.currency', 'Currency', required=True)
    boat_name = fields.Char('Boat Name')
    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)

    @api.one
    @api.constrains('from_date', 'to_date', 'weight', 'expected_price')
    def constrains(self):
        if self.from_date and self.to_date and self.to_date < self.from_date:
            raise ValidationError(_("From date can't start after to date!"))
        elif self.weight <= 0:
            raise ValidationError(_("Weight can not be lower than 0!"))
        elif self.expected_price <= 0:
            raise ValidationError(_("Expected price can not be lower than 0!"))

    @api.one
    @api.depends('contract_id', 'weight', 'unit_id', 'product_group_id')
    def compute_name(self):
        if self.contract_id and self.product_group_id and self.weight and self.unit_id:
            self.name = self.contract_id.name + ' ' + str(
                base.check_number(self, self.weight)) + ' ' + self.unit_id.name + ' ' + self.product_group_id.name
