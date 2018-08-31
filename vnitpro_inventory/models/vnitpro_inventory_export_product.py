# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

SHIFT = [('shift1', 'Shift 1'),
         ('shift2', 'Shift 2'),
         ('shift3', 'Shift 3')]

class InventoryExportProduct(models.Model):
    _name = "vnitpro.inventory.export.product"
    _rec_name = 'export_card_number'

    export_formality = fields.Many2one('vnitpro.inventory.export.formality.product','Export Formality', size=200, required=True, track_visibility="onchange")
    export_card_number = fields.Char('Export Card Number', size=50, required=True, track_visibility="onchange")
    export_date = fields.Date('Export Date', required=True, track_visibility="onchange")
    shift = fields.Selection(SHIFT, 'Shift', required=True, track_visibility="onchange")

    sender_id = fields.Many2one('vnitpro.department', 'Sender', required=True,
                                domain="[('id','!=',partners_id)]", track_visibility="onchange")
    employee_sender_id = fields.Many2one('vnitpro.employee', 'Employee Sender',
                                         domain="[('department_id','=',sender_id)]", required=True,
                                         track_visibility="onchange")
    sender_position = fields.Many2one('vnitpro.position', 'Position', related='employee_sender_id.position_id',
                                      readonly=True, track_visibility="onchange")
    partners_id = fields.Many2one('vnitpro.company', 'Partners', required=True, track_visibility="onchange")
    tranposter_id = fields.Many2one('vnitpro.company', 'Tranposter',required=True, track_visibility="onchange")
    car_number_id = fields.Many2one('vnitpro.company.car', 'Car Number', domain="[('company_id','=',tranposter_id)]",
                                    track_visibility="onchange")
    romooc_number_id = fields.Many2one('vnitpro.company.romooc', 'Romooc Number',
                                       domain="[('company_id','=',tranposter_id)]", track_visibility="onchange")
    move_order = fields.Char('Move Order', size=200, required=True, track_visibility="onchange")
    move_order_date = fields.Date('Move Order Date', required=True, track_visibility="onchange")
    warehouse_export_id = fields.Many2one('vnitpro.warehouse', 'Warehouse Export', required=True,
                                          track_visibility="onchange")
    stocker = fields.Char('Stocker', size=100, required=True, track_visibility="onchange")
    warehouse_come_id = fields.Many2one('vnitpro.warehouse', 'Warehouse Come', required=True,
                                        track_visibility="onchange")
    weighted_votes = fields.Char('Weighted Votes', size=100, required=True, track_visibility="onchange")
    weighted_votes_date = fields.Date('Weighted Votes Date', required=True, track_visibility="onchange")
    export_detail_ids = fields.One2many('vnitpro.inventory.export.product.detail', 'inventory_export_product_id',
                                        'Export Product')


class InventoryExportProductDetail(models.Model):
    _name = "vnitpro.inventory.export.product.detail"

    product_group_id = fields.Many2one('vnitpro.product.group', 'Product Group', required=True, track_visibility="onchange")
    product_id = fields.Many2one('vnitpro.product', 'Product', track_visibility="onchange",
                                       domain="[('product_group_id','=',product_group_id)]")
    style = fields.Char('Style', size=200, required=True, track_visibility="onchange")
    present_quantity = fields.Float('Present Quantity', required=True, track_visibility="onchange")
    unit = fields.Many2one('vnitpro.unit', 'Unit', related='product_group_id.unit_id', readonly=True,
                           track_visibility="onchange")
    number_of_packaging = fields.Integer('Number Of Packaging', required=True, track_visibility="onchange")
    lot_number = fields.Char('Lot Number', size=50, required=True, track_visibility="onchange")
    note = fields.Text('Note', size=200, track_visibility="onchange")
    inventory_export_product_id = fields.Many2one('vnitpro.inventory.export.product', 'Inventory Import Product',
                                                  ondelete="cascade")

    @api.one
    @api.constrains('present_quantity', 'number_of_packaging')
    def validate_quantity(self):
        if self.present_quantity <= 0:
            raise ValidationError(_('Quantity must be bigger than 0 !'))
        elif self.number_of_packaging <= 0:
            raise ValidationError(_('Number of packaging must be bigger than 0 !'))

class InventoryExportFormalityProduct(models.Model):
    _name = "vnitpro.inventory.export.formality.product"
    _inherit = "vnitpro.base.information"