# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

PRODUCT = [('standard_products', 'Standard Products'), ('product_defects', 'Product Defects')]
SHIFT = [('shift1', 'Shift 1'),
         ('shift2', 'Shift 2'),
         ('shift3', 'Shift 3')]


class InventoryImportProduct(models.Model):
    _name = "vnitpro.inventory.import.product"
    _rec_name = 'export_card_number'

    import_type = fields.Selection(PRODUCT, 'Import', required=True, track_visibility="onchange",
                                   default='standard_products')
    import_formality_standard = fields.Many2one('vnitpro.inventory.import.formality.product.standard',
                                                'Import Formality', size=200, track_visibility="onchange")
    import_formality_defects = fields.Many2one('vnitpro.inventory.import.formality.product.defects', 'Import Formality',
                                               size=200, track_visibility="onchange")
    export_card_number = fields.Char('Export Card Number', size=50, required=True, track_visibility="onchange")
    import_date = fields.Date('Import Date', required=True, track_visibility="onchange")
    shift = fields.Selection(SHIFT, 'Shift', required=True, track_visibility="onchange")
    sender_id = fields.Many2one('vnitpro.department', 'Sender', required=True, domain="[('id','!=',partners_id)]",
                                track_visibility="onchange")
    employee_sender_id = fields.Many2one('vnitpro.employee', 'Employee Sender',
                                         domain="[('department_id','=',sender_id)]", required=True,
                                         track_visibility="onchange")
    sender_position = fields.Many2one('vnitpro.position', 'Position', related='employee_sender_id.position_id',
                                      readonly=True, track_visibility="onchange")
    partners_id = fields.Many2one('vnitpro.department', 'Partners', required=True, domain="[('id','!=',sender_id)]",
                                  track_visibility="onchange")
    employee_partners_id = fields.Many2one('vnitpro.employee', 'Employee Partners',
                                           domain="[('department_id','=',partners_id)]", required=True,
                                           track_visibility="onchange")
    partners_position = fields.Char('Position', related='employee_partners_id.position_id.name', readonly=True,
                                    track_visibility="onchange")

    production_order = fields.Char('Production Order', size=200, required=True, track_visibility="onchange")
    production_order_date = fields.Date('Production Order Date', required=True, track_visibility="onchange")
    warehouse_id = fields.Many2one('vnitpro.warehouse', 'Warehouse', required=True, track_visibility="onchange")
    receipt_of_delivery = fields.Char('Receipt Of Delivery', size=200, required=True, track_visibility="onchange")
    receipt_of_delivery_date = fields.Date('Receipt Of Delivery Date', required=True, track_visibility="onchange")
    stocker_name = fields.Char('Stocker Name', size=200, required=True, track_visibility="onchange")
    import_detail_ids = fields.One2many('vnitpro.inventory.import.product.detail', 'inventory_import_product_id',
                                        'Product Detail List')


class InventoryImportProductDetail(models.Model):
    _name = "vnitpro.inventory.import.product.detail"

    product_group_id = fields.Many2one('vnitpro.product.group', 'Product Group', required=True,
                                       track_visibility="onchange")
    product_id = fields.Many2one('vnitpro.product', 'Product', track_visibility="onchange",
                                 domain="[('product_group_id','=',product_group_id)]")
    style = fields.Char('Style', size=200, required=True, track_visibility="onchange")
    quantity = fields.Float('Quantity', required=True, track_visibility="onchange", digits=(3, 2))
    unit = fields.Many2one('vnitpro.unit', 'Unit', related='product_group_id.unit_id', readonly=True,
                           track_visibility="onchange")
    number_of_packaging = fields.Integer('Number Of Packaging', required=True, track_visibility="onchange")
    lot_number = fields.Char('Lot Number', size=50, required=True, track_visibility="onchange")
    note = fields.Text('Note', size=200, track_visibility="onchange")
    inventory_import_product_id = fields.Many2one('vnitpro.inventory.import.product', 'Inventory Import Product',
                                                  ondelete="cascade")

    @api.one
    @api.constrains('quantity', 'number_of_packaging')
    def validate(self):
        if self.quantity <= 0:
            raise ValidationError(_('Quantity must be bigger than 0 !'))
        elif self.number_of_packaging <= 0:
            raise ValidationError(_('Number of packaging must be bigger than 0 !'))


class InventoryImportFormalityProductStandard(models.Model):
    _name = "vnitpro.inventory.import.formality.product.standard"
    _inherit = "vnitpro.base.information"


class InventoryImportFormalityProductDefects(models.Model):
    _name = "vnitpro.inventory.import.formality.product.defects"
    _inherit = "vnitpro.base.information"
