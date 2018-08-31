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


# # author: Tu Vo, model: project.py, module project
# # tác giả: Võ Tuấn Tú, model: project.py, module quản lý dự án

class Project(models.Model):
    _inherit = 'vnitpro.project'

    decision = fields.Char('Decision', track_visibility='onchange')
    approver = fields.Char('Approver', track_visibility='onchange')
    approval_date = fields.Date('Approval Date', track_visibility='onchange')
    approval_cost_before_vat = fields.Float('Approval Cost Before VAT', digits=(3, 2), track_invisibility='onchange')
    vat_2 = fields.Selection([(0, '0 %'), (5, '5 %'), (10, '10 %')], 'VAT %', default=0,
                             track_visibility='onchange')
    vat_cost_2 = fields.Float('VAT Cost', digits=(3, 2), compute='compute_vat_2_cost', readonly=True)
    approval_cost_after_vat = fields.Float('Approval Cost After VAT', digits=(3, 2), compute='compute_approval_cost',
                                           track_invisibility='onchange')
    funds = fields.Many2one('vnitpro.payment.capital', 'Funds', track_visibility='onchange')
    currency_2 = fields.Many2one('vnitpro.currency', 'Currency', track_visibility='onchange')
    confirm_status = fields.Selection([(1, 'Draft'), (2, 'Confirmed')], 'Confirm Status', default=1)
    confirm_contract_file_attachment_ids = fields.One2many(
        'vnitpro.base.attachment', 'confirm_project_id', 'Attach File')

    @api.one
    def confirm_project(self):
        if self.decision and self.approver and self.approval_date and self.approval_cost_before_vat and self.funds and self.currency_2:
            self.confirm_status = 2
        else:
            raise ValidationError(_("You have to fill all the form before confirm project!"))

    @api.one
    def cancel_confirm(self):
        self.confirm_status = 1

    @api.one
    @api.depends('approval_cost_before_vat', 'vat_2')
    def compute_vat_2_cost(self):
        self.vat_cost_2 = self.approval_cost_before_vat * self.vat_2 / 100

    @api.one
    @api.depends('approval_cost_before_vat', 'vat_cost')
    def compute_approval_cost(self):
        self.approval_cost_after_vat = self.vat_cost_2 + self.approval_cost_before_vat
