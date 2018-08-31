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


class GenProcurementListReport(models.TransientModel):
    _name = 'vnitpro.gen.procurement.list.report'
    _description = 'Generate Procurement List Report'

    name = fields.Char('Name', compute="_compute_name")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date', default=fields.Date.today())
    procurement_code = fields.Char('Procurement Code', size=255)
    procurement_name = fields.Char('Procurement Name', size=50)
    create_user = fields.Many2one('vnitpro.employee', 'Create User')

    @api.constrains('from_date', 'to_date')
    def validate_fromdate_todate(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError(_('To Date cannot be set before From Date'))

    def _compute_name(self):
        self.name = _("Generate Report")

    def count_procurement_ids(self):
        data = self.read(['from_date', 'to_date', 'procurement_code', 'procurement_name', 'create_user'])[0]
        domains = []
        if self.from_date:
            domains += [('create_date', '>=', self.from_date)]
        if self.to_date:
            domains += [('create_date', '<=', self.to_date)]
        if self.procurement_code:
            domains += [('code', 'ilike', self.procurement_code)]
        if self.procurement_name:
            domains += [('name', 'ilike', self.procurement_name)]
        if self.create_user:
            domains += [('create_uid', '=', self.create_user.res_user_id.id)]
        procurement_ids = self.env['vnitpro.procurement'].search(domains, order="create_date")
        data.update({'procurement_ids': procurement_ids.ids})
        return data

    @api.multi
    def view_pdf(self):
        data = self.count_procurement_ids()
        return self.env.ref('vnitpro_procurement.action_report_generate_procurement_list').report_action(self, data=data)

    @api.multi
    def print_excel(self):
        return self.env.ref('vnitpro_procurement.action_report_generate_procurement_list_xlsx').report_action(self)
