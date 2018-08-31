# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


# # author: Tu Vo, model: project.py, module project
# # tác giả: Võ Tuấn Tú, model: project.py, module quản lý dự án

class Project(models.Model):
    _name = 'vnitpro.project'
    _inherit = 'vnitpro.base.information'

    # project information

    code = fields.Char('Project Code', required=True, track_visibility='onchange')
    name = fields.Char('Project Name', required=True, track_visibility='onchange')
    employer = fields.Many2one('vnitpro.bidder', 'Employer', required=True, track_visibility='onchange')
    cost_before_vat = fields.Float('Cost Before VAT', digits=(3, 2), required=True, track_visibility='onchange')
    vat = fields.Selection([(0, '0 %'), (5, '5 %'), (10, '10 %')], 'VAT %', required=True, default=0,
                           track_visibility='onchange')
    vat_cost = fields.Float('VAT Cost', digits=(3, 2), compute='compute_vat_cost', readonly=True)
    cost_after_vat = fields.Float('Cost After VAT', digits=(3, 2), compute='compute_cost', readonly=True)
    currency = fields.Many2one('vnitpro.currency', 'Currency', required=True, track_visibility='onchange')
    status = fields.Selection(
        [(2, 'Pending'), (3, 'In Process'), (4, 'Finish'), (5, 'On Hold'), (6, 'Cancel')], 'Status', default=2)
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'project_id', 'Attach File')

    start_date = fields.Date('Start Date', required=True, track_visibility='onchange')
    end_date = fields.Date('End Date', required=True, track_visibility='onchange')
    expire_date = fields.Date('Expire Date', compute='compute_expire_date', store=True)

    @api.one
    @api.depends('end_date')
    def compute_expire_date(self):
        if self.end_date:
            self.expire_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')

    @api.one
    @api.depends('cost_before_vat', 'vat')
    def compute_vat_cost(self):
        self.vat_cost = self.cost_before_vat * self.vat / 100

    @api.one
    @api.depends('cost_before_vat', 'vat_cost')
    def compute_cost(self):
        self.cost_after_vat = self.vat_cost + self.cost_before_vat
