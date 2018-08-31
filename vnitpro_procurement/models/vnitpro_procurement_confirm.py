# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

VAT_COMFIRM = [('0', '0 %'), ('5', '5 %'), ('10', '10 %')]


class ProcurementConfirm(models.Model):
    _inherit = "vnitpro.procurement"

    # confirm
    code_confirm = fields.Char('Number Of Approval Decision', size=50, track_visibility="onchange")
    approver = fields.Many2one('vnitpro.employee', 'Approver', size=300, track_visibility="onchange",
                               domain="[('activate','=', 'usage'),('department_id.permission_approve','=', True)]")
    approval_date = fields.Date('Approval Date', track_visibility="onchange")
    before_tax = fields.Float('Before Tax', track_visibility="onchange", digits=(3, 2))
    vat_confirm = fields.Selection(VAT_COMFIRM, '% VAT', default='0')
    after_tax = fields.Float('After Tax', size=300, track_visibility="onchange",
                             compute='compute_after_tax', digits=(3, 2), store=True)
    money_tax = fields.Float('Money Tax', size=300, track_visibility="onchange",
                             compute='compute_money_tax', digits=(3, 2))
    currency_confirm_id = fields.Many2one('vnitpro.currency', 'Currency', size=300,
                                          track_visibility="onchange", domain="[('activate','=', 'usage')]")
    confirm_procurement_attachment_ids = fields.One2many(
        'vnitpro.base.attachment', 'confirm_procurement_id', 'Attach Files')
    confirm_status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')],
                                      'Confirm Status', default='draft')

    # procurement_state
    confirmed_procurement = fields.Boolean(
        'Confirmed Procurement', compute="_compute_check_confirm_procurement", store=True)

    @api.one
    @api.depends('before_tax', 'vat_confirm')
    def compute_money_tax(self):
        self.money_tax = self.before_tax * int(self.vat_confirm) / 100

    @api.one
    @api.depends('confirm_status')
    def _compute_check_confirm_procurement(self):
        if self.confirm_status == 'draft':
            self.confirmed_procurement = False
        else:
            self.confirmed_procurement = True

    @api.one
    @api.depends('before_tax', 'money_tax')
    def compute_after_tax(self):
        self.after_tax = self.before_tax + self.money_tax

    @api.multi
    def edit_confirm(self):
        procurement_confirm_view = self.env.ref('vnitpro_procurement.view_vnitpro_procurement_confirm_form', False)
        return {
            'name': _('Confirm Procurement'),
            'domain': [],
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'target': 'new',
            'views': [(procurement_confirm_view.id, 'form')],
            'view_id': procurement_confirm_view.id,
        }

    @api.multi
    @api.constrains('before_tax')
    def validate_from_before_tax(self):
        for record in self:
            if record.before_tax <= 0:
                raise ValidationError(_('Before Tax must be bigger than 0'))

    @api.multi
    @api.constrains('code_confirm')
    def _compute_special_character_code_confirm(self):
        if self.code_confirm:
            for record in self:
                if not re.match("^[a-zA-Z0-9_/\\\\]*$", record.code_confirm):
                    raise ValidationError(_(
                        "Invalid Number Of Approval Decision, please try again ( Number Of Approval Decision only contains letters, numbers and character: / , \\ , _ ) ."))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    confirm_procurement_id = fields.Many2one('vnitpro.procurement', 'Confirm Procurement', ondelete='cascade')
