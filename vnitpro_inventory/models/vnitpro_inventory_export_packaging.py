# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InventoryExportPackaging(models.Model):
    _name = "vnitpro.inventory.export.packaging"
    _rec_name = 'export_card_number'

    export_formality = fields.Many2one('vnitpro.inventory.export.formality.packaging', 'Import Formality', size=200,
                                       required=True, track_visibility="onchange")
    export_card_number = fields.Char('Export Card Number', size=50, required=True, track_visibility="onchange")
    export_date = fields.Date('Export Date', required=True, track_visibility="onchange")

    sender_id = fields.Many2one('vnitpro.department', 'Sender', required=True, track_visibility="onchange")
    employee_sender_id = fields.Many2one('vnitpro.employee', 'Employee Sender',
                                         domain="[('department_id','=',sender_id)]", required=True,
                                         track_visibility="onchange")
    sender_position = fields.Char('Position', related='employee_sender_id.position_id.name', required=True,
                                  track_visibility="onchange")
    partners_id = fields.Many2one('vnitpro.department', 'Partners', required=True, domain="[('id','!=',sender_id)]",
                                  track_visibility="onchange")
    employee_partners_id = fields.Many2one('vnitpro.employee', 'Employee Partners',
                                           domain="[('department_id','=',partners_id)]", required=True,
                                           track_visibility="onchange")
    partners_position = fields.Char('Position', related='employee_partners_id.position_id.name', required=True,
                                    track_visibility="onchange")

    output_order = fields.Char('Output Order', size=200, required=True, track_visibility="onchange")
    output_order_date = fields.Date('Output Order Date', required=True, track_visibility="onchange")
    warehouse_export_id = fields.Many2one('vnitpro.warehouse', 'Export Warehouse', required=True,
                                          track_visibility="onchange")
    warehouse_import_id = fields.Many2one('vnitpro.warehouse', 'Import Warehouse', required=True,
                                          track_visibility="onchange")
    stocker_name = fields.Char('Stocker Name', size=200, required=True, track_visibility="onchange")
    export_detail_ids = fields.One2many('vnitpro.inventory.export.packaging.detail', 'inventory_export_packaging_id',
                                        'Packaging Detail List')



class InventoryExportProductDetail(models.Model):
    _name = "vnitpro.inventory.export.packaging.detail"

    packaging_id = fields.Many2one('vnitpro.packaging', 'Packaging', required=True, track_visibility="onchange")
    unit = fields.Many2one('vnitpro.unit', 'Unit', required=True, track_visibility="onchange")
    quantity = fields.Float('Quantity', size=50, required=True, track_visibility="onchange")
    lot_number = fields.Char('Lot Number', size=50, required=True, track_visibility="onchange")
    seri_number = fields.Char('Seri Number', size=50, required=True, track_visibility="onchange")
    note = fields.Text('Note', size=200, track_visibility="onchange")
    inventory_export_packaging_id = fields.Many2one('vnitpro.inventory.export.packaging', 'Inventory Export Packaging',
                                                    ondelete="cascade")

    @api.one
    @api.constrains('quantity')
    def validate(self):
        if self.quantity <= 0:
            raise ValidationError(_('Quantity must be bigger than 0 !'))


class InventoryExportFormalityPackaging(models.Model):
    _name = "vnitpro.inventory.export.formality.packaging"
    _inherit = "vnitpro.base.information"
