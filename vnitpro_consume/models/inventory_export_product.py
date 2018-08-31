# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InventoryExportProduct(models.Model):
    _inherit = "vnitpro.inventory.export.product"

    delivery_plan_id = fields.Many2one('vnitpro.delivery.plan', 'Delivery Plan', required=True,
                                       track_visibility="onchange")
    contract_id = fields.Many2one('vnitpro.product.information', 'Contract', required=True,
                                  track_visibility="onchange",domain="[('delivery_plan_id','=',delivery_plan_id)]")
    order_id = fields.Many2one('vnitpro.order', 'Order', required=True,
                                  track_visibility="onchange",domain="[('contract_id','=',contract_id)]")
