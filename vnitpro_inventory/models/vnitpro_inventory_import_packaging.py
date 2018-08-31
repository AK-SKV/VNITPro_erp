# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InventoryImportPackaging(models.Model):
    _name = "vnitpro.inventory.import.packaging"
    _rec_name = 'export_card_number'

    import_formality = fields.Many2one('vnitpro.inventory.import.formality.packaging', 'Import Formality', size=200,
                                       required=True, track_visibility="onchange")
    export_card_number = fields.Char('Export Card Number', size=50, required=True, track_visibility="onchange")
    import_date = fields.Date('Import Date', required=True, track_visibility="onchange")

    sender_id = fields.Many2one('vnitpro.department', 'Sender', required=True, track_visibility="onchange")
    employee_sender_id = fields.Many2one('vnitpro.employee', 'Employee Sender',
                                         domain="[('department_id','=',sender_id)]", required=True,
                                         track_visibility="onchange")
    sender_position = fields.Char('Position', related='employee_sender_id.position_id.name', readonly=True,
                                  track_visibility="onchange")
    partners_id = fields.Many2one('vnitpro.department', 'Partners', required=True,domain="[('id','!=',sender_id)]", track_visibility="onchange")
    employee_partners_id = fields.Many2one('vnitpro.employee', 'Employee Partners',
                                           domain="[('department_id','=',partners_id)]", required=True,
                                           track_visibility="onchange")
    partners_position = fields.Char('Position', related='employee_partners_id.position_id.name', readonly=True,
                                    track_visibility="onchange")

    input_order = fields.Char('Input Order', size=200, required=True, track_visibility="onchange")
    input_order_date = fields.Date('Input Order Date', required=True, track_visibility="onchange")
    warehouse_id = fields.Many2one('vnitpro.warehouse', 'Warehouse', required=True, track_visibility="onchange")
    receipt_of_delivery = fields.Char('Receipt Of Delivery', size=200, required=True, track_visibility="onchange")
    receipt_of_delivery_date = fields.Date('Receipt Of Delivery Date', required=True, track_visibility="onchange")
    stocker_name = fields.Char('Stocker Name', size=200, required=True, track_visibility="onchange")
    import_detail_ids = fields.One2many('vnitpro.inventory.import.packaging.detail', 'inventory_import_packaging_id',
                                        'Packaging Detail List')


class InventoryImportProductDetail(models.Model):
    _name = "vnitpro.inventory.import.packaging.detail"

    packaging_id = fields.Many2one('vnitpro.packaging', 'Packaging', required=True, track_visibility="onchange")
    unit = fields.Many2one('vnitpro.unit', 'Unit', required=True, track_visibility="onchange")
    quantity = fields.Float('Quantity', size=50, required=True, track_visibility="onchange")
    lot_number = fields.Char('Lot Number', size=50, required=True, track_visibility="onchange")
    seri_number = fields.Char('Seri Number', size=50, required=True, track_visibility="onchange")
    note = fields.Text('Note', size=200, track_visibility="onchange")
    inventory_import_packaging_id = fields.Many2one('vnitpro.inventory.import.packaging', 'Inventory Import Packaging',
                                                    ondelete="cascade")

    @api.one
    @api.constrains('quantity')
    def validate(self):
        if self.quantity <= 0:
            raise ValidationError(_('Quantity must be bigger than 0 !'))


class InventoryImportFormalityPackaging(models.Model):
    _name = "vnitpro.inventory.import.formality.packaging"
    _inherit = "vnitpro.base.information"
