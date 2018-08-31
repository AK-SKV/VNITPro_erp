# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
import logging
import re
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

TYPE_CONTRACT = [('1', 'By Fixed Price'), ('2', 'By Adjusted Value'), ('3', 'By Time'), ('4', 'By Package')]


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    code_advisory = fields.Char('Code Advisory', size=50,  track_visibility="onchange")
    name_advisory = fields.Char('Name Advisory', size=300,  track_visibility="onchange")
    bidder_a = fields.Many2one('vnitpro.bidder', 'Bidder A',  track_visibility="onchange",
                               domain="[('id','!=',bidder_b),('activate','=','usage')]")
    bidder_b = fields.Many2one('vnitpro.bidder', 'Bidder B',  track_visibility="onchange",
                               domain="[('id','!=',bidder_a),('activate','=','usage')]")
    type_of_contract_advisory = fields.Selection(TYPE_CONTRACT, 'Type Of Contract')
    contract_after_vat = fields.Float('Contract After VAT', size=50, track_visibility="onchange", digits=(3, 2))
    currency_advisory_id = fields.Many2one('vnitpro.currency', 'Currency', size=300,
                                           track_visibility="onchange", domain="[('activate','=', 'usage')]")
    from_date_ad = fields.Date('From Date',  track_visibility="onchange")
    to_date_ad = fields.Date('To Date',  track_visibility="onchange")
    funds_advisory = fields.Many2many(comodel_name='vnitpro.payment.capital', relation="funds_advisory_payment_capital", string='Funds',
                                      track_visibility="onchange", domain="[('activate','=', 'usage')]")
    confirmed = fields.Boolean('Confirmed')
    created_advision = fields.Boolean('Created Advisory Procurement')
    advisory_procurement_attachment_ids = fields.One2many(
        'vnitpro.base.attachment', 'advisory_procurement_id', 'Attach Files')

    @api.multi
    def edit_advisory(self):
        procurement_advisory_view = self.env.ref('vnitpro_procurement.view_vnitpro_procurement_advisory_form', False)
        return {
            'name': _('Advisory Procurement'),
            'domain': [],
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'target': 'new',
            'views': [(procurement_advisory_view.id, 'form')],
            'view_id': procurement_advisory_view.id,
        }

    @api.multi
    def delete_advisory(self):
        self.code_advisory = False
        self.name_advisory = False
        self.bidder_a = False
        self.bidder_b = False
        self.type_of_contract_advisory = False
        self.contract_after_vat = False
        self.currency_advisory_id = False
        self.from_date_ad = False
        self.to_date_ad = False
        self.code_advisory = False
        self.funds_advisory = False
        self.confirmed = False

    @api.multi
    def save_refresh(self):
        return False

    @api.multi
    @api.constrains('code_advisory')
    def _compute_special_character_code_advisory(self):
        if self.code_advisory:
            for record in self:
                if not re.match("^[a-zA-Z0-9_/\\\\]*$", record.code_advisory):
                    raise ValidationError(_(
                        "Invalid Code Advisory, please try again ( Code Advisory only contains letters, numbers and character: / , \\ , _ ) ."))

    @api.multi
    @api.constrains('contract_after_vat')
    def validate_from_contract_after_vat(self):
        for record in self:
            if record.contract_after_vat <= 0:
                raise ValidationError(_('Contract After VAT must be bigger than 0'))

    @api.one
    @api.constrains('from_date_ad', 'to_date_ad')
    def validate_from_date_to_date(self):
        if self.from_date_ad and self.to_date_ad:
            if self.from_date_ad > self.to_date_ad:
                raise ValidationError(_('To Date cannot be set before From Date !'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    advisory_procurement_id = fields.Many2one('vnitpro.procurement', 'Advisory Procurement', ondelete='cascade')
