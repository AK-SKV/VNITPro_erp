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

_logger = logging.getLogger(__name__)


class GenImportProductReport(models.TransientModel):
    _name = 'vnitpro.gen.import.product.report'
    _description = 'Generate Import Product Report'
    _rec_name = "name"

    name = fields.Char('Name', compute="_compute_name")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date', default=fields.Date.today())


    @api.constrains('from_date', 'to_date')
    def validate_fromdate_todat(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError(_('To Date cannot be set before From Date'))

    def _compute_name(self):
        self.name = _("Generate Report")

    def count_import_card_ids(self):
        data = self.read(['from_date', 'to_date'])[0]
        import_card_list_ids = self.env['vnitpro.inventory.import.product.detail'].search(
            [('inventory_import_product_id.import_date', '>=', self.from_date),
             ('inventory_import_product_id.import_date', '<=', self.to_date)])
        data.update({'import_card_ids': import_card_list_ids.ids})
        return data

    @api.multi
    def view_pdf(self):
        data = self.count_import_card_ids()
        return self.env.ref('vnitpro_inventory.action_report_generate_import_product').report_action(self, data=data)

