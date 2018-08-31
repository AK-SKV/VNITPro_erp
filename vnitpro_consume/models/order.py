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

_logger = logging.getLogger(__name__)


class Order(models.Model):
    _name = 'vnitpro.order'
    _inherit = 'mail.thread'
    _rec_name = 'code'

    code = fields.Char('Notification Number', required=True, track_visibility='onchange')
    sign_date = fields.Date('Sign Date', required=True, track_visibility='onchange')
    delivery_plan_id = fields.Many2one('vnitpro.delivery.plan', 'Plan Number', required=True,
                                       track_visibility='onchange')
    contract_id = fields.Many2one('vnitpro.product.information', 'Contract', required=True, track_visibility='onchange',
                                  domain="[('delivery_plan_id', '=', delivery_plan_id)]")
    customer_name = fields.Char('Customer Name', related='contract_id.customer', readonly=True,
                                track_visibility='onchange')
    boat_name = fields.Char('Boat Name', related='contract_id.boat_name', track_visibility='onchange')
    queue_speed = fields.Char('Queue Speed', required=True, track_visibility='onchange')
    delivery_place_id = fields.Many2one('vnitpro.delivery.place', required=True, track_visibility='onchange',
                                        domain=[('activate', '=', 'usage')])
    bonus_penalize_lvl = fields.Char('Bonus/Penalize Level', required=True, track_visibility='onchange')
    date_arrived = fields.Date('Date Arrived', required=True, track_visibility='onchange')
    by_lc = fields.Char('By L/C', required=True, track_visibility='onchange')
    delivery_condition = fields.Char('Delivery Condition', required=True, track_visibility='onchange')
    delivery_unit_id = fields.Many2one('vnitpro.delivery.unit', 'Delivery Unit', required=True,
                                       track_visibility='onchange', domain=[('activate', '=', 'usage')])
    inspection_unit_id = fields.Many2one('vnitpro.inspection.unit', 'Inspection Unit', required=True,
                                         track_visibility='onchange', domain=[('activate', '=', 'usage')])
    order_detail_ids = fields.One2many('vnitpro.order.detail', 'order_id', 'Order Detail')
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'order_id', 'Attachment Files')
    status = fields.Selection([('draft', 'Draft'),
                               ('done', 'Done')], 'Status', default='draft', track_visibility='onchange')
    _sql_constraints = [('unique_contract', 'unique(contract_id)', 'The order already exists!')]

    @api.one
    @api.constrains('sign_date', 'date_arrived')
    def constrains(self):
        if self.sign_date > self.date_arrived:
            raise ValidationError(_("Date arrived can't start before sign date!!"))

    @api.multi
    @api.onchange('contract_id')
    def change_contract(self):
        if self.contract_id:
            order_detail = []
            record = {
                'product_group_id': self.contract_id.product_group_id.id,
                'quantity': self.contract_id.weight,
            }
            order_detail.append(record)
            self.order_detail_ids = order_detail


class OrderDetail(models.Model):
    _name = 'vnitpro.order.detail'
    _inherit = 'mail.thread'

    order_id = fields.Many2one('vnitpro.order', 'Order', required=True, ondelete='cascade')
    product_group_id = fields.Many2one('vnitpro.product.group', readonly=True)
    quantity = fields.Float('Quantity', readonly=True)
    unit_id = fields.Many2one('vnitpro.unit', related='product_group_id.unit_id', readonly=True)
    unit_price = fields.Float('Unit Price', required=True)
    currency_id = fields.Many2one('vnitpro.currency', 'Currency', required=True)
    price = fields.Float('Price', compute='compute_price')
    tax_ids = fields.Many2many('vnitpro.taxes', string='Taxes')
    total_price = fields.Float('Total Price', compute='compute_price')

    @api.multi
    @api.depends('unit_price', 'quantity', 'tax_ids')
    def compute_price(self):
        self.total_price = self.price = self.unit_price * self.quantity
        for tax in self.tax_ids:
            self.total_price += self.price * tax.value / 100

    @api.one
    @api.constrains('unit_price')
    def constrains(self):
        if self.unit_price <= 0:
            raise ValidationError(_("Price can not be lower than 0!"))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    order_id = fields.Many2one('vnitpro.order', 'Order', ondelete='cascade')
