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


class GenContractListReport(models.TransientModel):
    _name = 'vnitpro.gen.contract.list.report'
    _description = 'Generate Contract List Report'
    _rec_name = "name"

    name = fields.Char('Name', compute='compute_name')
    contract_code = fields.Char('Contract Code', size=255)
    contract_name = fields.Char('Contract Name', size=50)
    contract_status = fields.Selection([('pending', 'Pending'),
                                        ('in_process', 'In Process'),
                                        ('liquidated', 'Liquidated'),
                                        ('finalized', 'Finalized'),
                                        ('on_hold', 'On Hold'),
                                        ('cancel', 'Cancel')], 'Status')
    bidder_a = fields.Many2one("vnitpro.bidder", "Bidder A", track_visibility='onchange',
                               domain="[('id','!=',bidder_b)]")
    bidder_b = fields.Many2one("vnitpro.bidder", "Bidder B", track_visibility='onchange',
                               domain="[('id','!=',bidder_a)]")
    contract_type_id = fields.Many2one('vnitpro.contract.type', 'Contract Type', track_visibility='onchange')
    create_user = fields.Many2one('vnitpro.employee', 'Create User')

    def count_contract_ids(self):
        data = self.read(['contract_code', 'contract_name', 'contract_status', 'bidder_a', 'bidder_b', 'contract_type_id',
                          'create_user'])[0]
        domains = []
        if self.contract_code:
            domains += [('code', 'ilike', self.contract_code)]
        if self.contract_name:
            domains += [('name', 'ilike', self.contract_name)]
        if self.contract_status:
            domains += [('status', '=', self.contract_status)]
        if self.bidder_a:
            domains += [('bidder_a', '=', self.bidder_a.id)]
        if self.bidder_b:
            domains += [('bidder_b', '=', self.bidder_b.id)]
        if self.contract_type_id:
            domains += [('contract_type_id', '=', self.contract_type.id)]
        if self.create_user:
            domains += [('create_uid', '=', self.create_user.res_user_id.id)]
        contract_ids = self.env['vnitpro.contract'].search(domains, order="create_date")
        data.update({'contract_ids': contract_ids.ids})
        return data

    @api.multi
    def view_pdf(self):
        data = self.count_contract_ids()
        return self.env.ref('vnitpro_contract.action_report_generate_contract_list').report_action(self, data=data)

    @api.multi
    def print_excel(self):
        data = self.count_contract_ids()
        return self.env.ref('vnitpro_contract.action_report_generate_contract_list_xlsx').report_action(self)

    @api.one
    def compute_name(self):
        self.name = (_("Generate Report"))
