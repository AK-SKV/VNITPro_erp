# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    negotiation_list_ids = fields.One2many('vnitpro.negotiation.result', 'procurement_id', 'Negotiation Results List')
    completed_import_negotiation_list = fields.Boolean('Completed Import Negotiation Results List')


class NegotiationResult(models.Model):
    _name = "vnitpro.negotiation.result"
    _rec_name = 'ranking_list_id'

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', ondelete="cascade")
    ranking_list_id = fields.Many2one('vnitpro.ranking.list', 'Bid Profile', required=True)
    negotiation_result = fields.Char('Negotiation Result', size=200, required=True)
    after_tax = fields.Float('After Tax', size=50, track_visibility="onchange",
                             digits=(3, 2), related="procurement_id.after_tax", required=True)
    the_negotiated_price_includes_vat = fields.Float(
        'The Negotiated Price Includes VAT', size=50, required=True, digits=(3, 2))
    price_difference = fields.Float('Price Difference', size=50, digits=(3, 2),
                                    required=True, compute='compute_price_difference')
    date_negotiation = fields.Date('Date Negotiation', track_visibility="onchange", required=True)
    negotiation_team_leader = fields.Many2one('vnitpro.employee', 'Negotiation Team Leader',
                                              domain="[('activate','=','usage')]", required=True)
    negotiation_team_member = fields.Many2one('vnitpro.employee', 'Negotiation Team Member',
                                              domain="[('activate','=','usage')]")
    note = fields.Text('Note', size=500)
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'negotation_result_id', 'Attach Files')

    @api.multi
    @api.constrains('the_negotiated_price_includes_vat')
    def validate_the_negotiated_price_includes_vat(self):
        for record in self:
            if record.the_negotiated_price_includes_vat <= 0:
                raise ValidationError(_('The Negotiated Price Includes VAT must be bigger than 0 !'))

    @api.one
    @api.depends('after_tax', 'the_negotiated_price_includes_vat')
    def compute_price_difference(self):
        self.price_difference = abs(self.after_tax - self.the_negotiated_price_includes_vat)


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    negotation_result_id = fields.Many2one('vnitpro.negotiation.result', 'Negotiation Result', ondelete='cascade')
