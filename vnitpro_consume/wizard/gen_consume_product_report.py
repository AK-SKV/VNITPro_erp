# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re, datetime
import logging

_logger = logging.getLogger(__name__)


class GenConsumeProductReport(models.TransientModel):
    _name = 'vnitpro.gen.consume.product.report'
    _description = 'Generate Consume Product Report'
    _rec_name = "name"

    name = fields.Char('Name', compute='compute_name')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    def count_export_card_ids(self):
        data = self.read(['start_date', 'end_date'])[0]
        export_card_list_ids = self.env['vnitpro.inventory.export.product.detail'].search(
            [('inventory_export_product_id.export_date', '>=', self.start_date),
             ('inventory_export_product_id.export_date', '<=', self.end_date)])
        direct_export_card_list_ids = self.env['vnitpro.direct.import.product.detail'].search(
            [('direct_import_product_id.export_date', '>=', self.start_date),
             ('direct_import_product_id.export_date', '<=', self.end_date)])
        data.update({'export_card_ids': export_card_list_ids.ids,
                     'direct_export_card_list_ids': direct_export_card_list_ids.ids})
        return data

    @api.multi
    def view_pdf(self):
        data = self.count_export_card_ids()
        return self.env.ref('vnitpro_consume.action_report_generate_consume_product').report_action(self, data=data)

    @api.multi
    def print_excel(self):
        return True

    @api.one
    def compute_name(self):
        self.name = (_("Consume Product Report"))
