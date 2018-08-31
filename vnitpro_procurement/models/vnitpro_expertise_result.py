# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

RESULT = [(1, 'Won'), (2, 'Lose')]


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    expertise_result_ids = fields.One2many('vnitpro.expertise.result', 'procurement_id', 'Expertise Results')
    completed_expertise_bidder_selection = fields.Boolean('Completed Expertise Bidder Selection')


class ExpertiseResult(models.Model):
    _name = "vnitpro.expertise.result"

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', required=True, ondelete="cascade")
    negotiation_result_id = fields.Many2one('vnitpro.negotiation.result', 'Bid Profile', required=True)
    expertise_start_date = fields.Date('Expertise Start Date', track_visibility="onchange", required=True)
    expertise_end_date = fields.Date('Expertise End Date', track_visibility="onchange", required=True)
    expertise_results = fields.Selection(RESULT, 'Expertise Results', required=True, default=1)
    exposure_price_with_vat = fields.Float('Exposure Price With VAT', size=50, digits=(3, 2), required=True)
    number_of_the_selected_bid = fields.Char('Number Of The Selected Bid', size=20, required=True)
    decided_date = fields.Date('Decided Date', track_visibility="onchange", required=True)
    expertise_team_leader = fields.Many2one('vnitpro.employee', 'Expertise Team Leader',
                                            domain="[('activate','=','usage')]", required=True)
    expertise_team_member = fields.Many2one('vnitpro.employee', 'Expertise Team Member',
                                            domain="[('activate','=','usage')]", required=True)
    note = fields.Text('Note', size=500)
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'expertise_result_id', 'Attach Files')

    _sql_constraints = [
        ('uniq_negotiation_result', 'unique(procurement_id,negotiation_result_id)',
         'Bid Profile must be unique per Expertise Results'),
        ('uniq_expertise_results', 'unique(procurement_id,expertise_results)',
         'Only have one bid profile won per procurement, please double check again')
    ]

    @api.one
    @api.constrains('expertise_start_date', 'expertise_end_date')
    def validate_from_date_to_date(self):
        if self.expertise_start_date and self.expertise_end_date:
            if self.expertise_start_date > self.expertise_end_date:
                raise ValidationError(_('Expertise Start Date cannot be set before Expertise End Date !'))

    @api.one
    @api.constrains('exposure_price_with_vat')
    def validate_exposure_price_with_vat(self):
        if self.exposure_price_with_vat <= 0:
            raise ValidationError(_('Exposure Price With VAT must be bigger than 0 !'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    expertise_result_id = fields.Many2one('vnitpro.expertise.result', 'Expertise Result', ondelete='cascade')
