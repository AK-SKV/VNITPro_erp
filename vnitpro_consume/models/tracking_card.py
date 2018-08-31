# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re, operator
import logging

_logger = logging.getLogger(__name__)


class TrackingCard(models.Model):
    _name = 'vnitpro.tracking.card'

    name = fields.Char('Name', compute='compute_name')
    delivery_plan_id = fields.Many2one('vnitpro.delivery.plan', 'Delivery Plan', required=True)
    contract_id = fields.Many2one('vnitpro.product.information', 'Contract',
                                  domain="[('delivery_plan_id','=',delivery_plan_id)]", required=True)
    order_id = fields.Many2one('vnitpro.order', 'Order',
                               domain="[('contract_id','=',contract_id),('status','=','draft')]", required=True)
    customer_name = fields.Char('Customer Name', related='order_id.customer_name', readonly=True)
    product_group_id = fields.Many2one('vnitpro.product.group', 'Product', related='contract_id.product_group_id',
                                       readonly=True)
    delivery_formality_id = fields.Many2one('vnitpro.delivery.formality', 'Delivery Formality',
                                            related='contract_id.delivery_formality_id', readonly=True)
    weight_needed = fields.Float('Weight Needed', related='contract_id.weight', readonly=True)
    unit_id = fields.Many2one('vnitpro.unit', 'Unit', related='product_group_id.unit_id', readonly=True)
    expected_price = fields.Float('Expected Price', related='contract_id.expected_price', readonly=True)
    currency_id = fields.Many2one('vnitpro.currency', 'Currency', readonly=True)
    tracking_card_information_ids = fields.One2many('vnitpro.tracking.card.information', 'tracking_card_id',
                                                    'Tracking Card Information')
    total_weight_delivery = fields.Float('Total Weight Delivery', compute='compute_total', track_visibility='onchange')
    total_weight_left = fields.Float('Total Weight Left', compute='compute_total', track_visibility='onchange')
    total_cost = fields.Float('Total Cost', compute='compute_total', track_visibility='onchange')
    status = fields.Selection([('draft', 'Draft'),
                               ('done', 'Done')], 'Status', default='draft', track_visibility='onchange')

    _sql_constraints = [('unique_contract', 'unique(contract_id)', 'The tracking card already exists!')]

    @api.multi
    def confirm_order(self):
        self.status = 'done'
        self.order_id.status = 'done'

    @api.multi
    def check_product(self):
        self.tracking_card_information_ids = False
        for record in self.order_id.order_detail_ids:
            self.currency_id = record.currency_id
            unit_price = record.unit_price
            break
        export_card_list = []
        weight_left = self.weight_needed
        inventory_export_cards = self.env['vnitpro.inventory.export.product.detail'].search(
            [('inventory_export_product_id.contract_id', '=', self.contract_id.id),
             ('product_group_id', '=', self.product_group_id.id),
             ('inventory_export_product_id.order_id', '=', self.order_id.id)])
        direct_export_cards = self.env['vnitpro.direct.import.product.detail'].search(
            [('direct_import_product_id.contract_id', '=', self.contract_id.id),
             ('product_group_id', '=', self.product_group_id.id),
             ('direct_import_product_id.order_id', '=', self.order_id.id)])
        for record in inventory_export_cards:
            export_card = {
                'export_card_number': record.inventory_export_product_id.export_card_number,
                'export_date': record.inventory_export_product_id.export_date,
                'product_group_id': record.product_group_id,
                'weight_delivery': record.present_quantity,
                'currency_id': self.currency_id.id,
                'cost': record.present_quantity * unit_price,
            }
            export_card_list.append(export_card)
        for record in direct_export_cards:
            export_card = {
                'export_card_number': record.direct_import_product_id.export_card_number,
                'export_date': record.direct_import_product_id.export_date,
                'product_group_id': record.product_group_id,
                'weight_delivery': record.present_quantity,
                'currency_id': self.currency_id.id,
                'cost': record.present_quantity * unit_price,
            }
            export_card_list.append(export_card)
        export_card_list.sort(key=operator.itemgetter('export_date'))
        for record in export_card_list:
            weight_left -= record['weight_delivery']
            record.update({'weight_left': weight_left})
        self.tracking_card_information_ids = export_card_list

    @api.one
    @api.depends('order_id')
    def compute_name(self):
        self.name = _('Tracking Card') + ' ' + self.order_id.code

    @api.multi
    @api.depends('tracking_card_information_ids')
    def compute_total(self):
        for record in self.tracking_card_information_ids:
            self.total_weight_delivery += record.weight_delivery
            self.total_weight_left = record.weight_left
            self.total_cost += record.cost


class TrackingCardInformation(models.Model):
    _name = 'vnitpro.tracking.card.information'

    tracking_card_id = fields.Many2one('vnitpro.tracking.card', 'Tracking Card', required=True, ondelete='cascade')

    export_card_number = fields.Char('Export Card Number', readonly=True)
    export_date = fields.Date('Export Date', readonly=True)
    product_group_id = fields.Many2one('vnitpro.product.group', 'Product', readonly=True)
    unit_id = fields.Many2one('vnitpro.unit', 'Unit', related='product_group_id.unit_id', readonly=True)
    weight_delivery = fields.Float('Weight Delivery', readonly=True)
    weight_left = fields.Float('Weight Left', readonly=True)
    cost = fields.Float('Cost', readonly=True)
    currency_id = fields.Many2one('vnitpro.currency', 'Currency', readonly=True)
    reversed = fields.Float('Reversed', compute='compute_reversed')

    @api.one
    def compute_reversed(self):
        import_quantity = export_quantity = 0
        import_inven_list = self.env['vnitpro.inventory.import.product.detail'].search(
            [('product_group_id', '=', self.product_group_id.id),
             ('inventory_import_product_id.import_date', '<=', self.export_date)])
        export_inven_list = self.env['vnitpro.inventory.export.product.detail'].search(
            [('product_group_id', '=', self.product_group_id.id),
             ('inventory_export_product_id.export_date', '<=', self.export_date)])
        for record in import_inven_list:
            import_quantity += record.quantity
        for record in export_inven_list:
            export_quantity += record.present_quantity
        self.reversed = import_quantity - export_quantity
