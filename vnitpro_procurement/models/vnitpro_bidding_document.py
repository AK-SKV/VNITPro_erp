# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    bidding_document_code = fields.Char('Bidding Document Code', size=50)
    bidding_document_name = fields.Char('Bidding Document Name', size=200)
    release_time_bidding = fields.Date('Release Time', track_visibility="onchange")
    bid_closing_date = fields.Date('Bid Closing Date', track_visibility="onchange")
    date_open_file = fields.Date('Date Open File', track_visibility="onchange")
    review_start = fields.Date('Review Start Date', track_visibility="onchange")
    review_end = fields.Date('Review End Date', track_visibility="onchange")
    new_history = fields.Date('New History', track_visibility="onchange")
    confirmed_bidding_document = fields.Boolean('Confirmed Bidding Document')
    created_bidding_document = fields.Boolean('Created Bidding Document')
    bidding_document_attachment_ids = fields.One2many('vnitpro.base.attachment', 'bidding_document_id', 'Attach Files')

    @api.multi
    def edit_bidding(self):
        procurement_bidding_document_view = self.env.ref(
            'vnitpro_procurement.view_vnitpro_procurement_bidding_document_form', False)
        return {
            'name': _('Bidding Document'),
            'domain': [],
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'target': 'new',
            'views': [(procurement_bidding_document_view.id, 'form')],
            'view_id': procurement_bidding_document_view.id,
        }

    @api.multi
    def delete_bidding(self):
        self.bidding_document_code = False
        self.bidding_document_name = False
        self.release_time_bidding = False
        self.bid_closing_date = False
        self.date_open_file = False
        self.review_start = False
        self.review_end = False
        self.new_history = False
        self.confirmed_bidding_document = False

    @api.multi
    @api.constrains('bidding_document_code')
    def _compute_special_character_bidding_document_code(self):
        if self.bidding_document_code:
            for record in self:
                if not re.match("^[a-zA-Z0-9_/\\\\]*$", record.bidding_document_code):
                    raise ValidationError(
                        _("Invalid Bidding Document Code, please try again ( Bidding Document Code only contains letters, numbers and character: / , \\ , _ ) ."))

    @api.one
    @api.constrains('release_time_bidding', 'bid_closing_date')
    def validate_release_time_bidding_bid_closing_date(self):
        if self.release_time_bidding and self.bid_closing_date and self.release_time_bidding > self.bid_closing_date:
            raise ValidationError(_('Bid Closing Date cannot be set before Release Time !'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    bidding_document_id = fields.Many2one('vnitpro.procurement', 'Bidding Document', ondelete='cascade')
