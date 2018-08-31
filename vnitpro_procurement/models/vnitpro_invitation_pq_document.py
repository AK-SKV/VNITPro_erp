# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
import re
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    code_profile = fields.Char('Profile Code', size=50, track_visibility="onchange")
    name_profile = fields.Char('Profile Name', size=255, track_visibility="onchange")
    release_time = fields.Date('Release Time', track_visibility="onchange")
    bid_submission_deadline = fields.Date('Bid Submission Deadline', track_visibility="onchange")
    creator = fields.Many2one('res.users', 'Creator', default=lambda self: self.env.user, store=True)
    approved = fields.Boolean('Approved By The Director')
    created_invitation_pq_doc = fields.Boolean('Created Invitation PQ Documents')
    invitation_pq_document_attachment_ids = fields.One2many('vnitpro.base.attachment',
                                                            'invitation_pq_document_procurement_id', 'Attach Files')

    @api.multi
    def edit_invitation(self):
        procurement_invitation_view = self.env.ref(
            'vnitpro_procurement.view_vnitpro_procurement_invitation_form', False)
        return {
            'name': _('Invitation PQ Documents'),
            'domain': [],
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'target': 'new',
            'views': [(procurement_invitation_view.id, 'form')],
            'view_id': procurement_invitation_view.id,
        }

    @api.multi
    def delete_invitation(self):
        self.code_profile = False
        self.name_profile = False
        self.release_time = False
        self.bid_submission_deadline = False
        self.creator = False
        self.approved = False

    @api.multi
    @api.constrains('code_profile')
    def _compute_special_character_code_profile(self):
        if self.code_profile:
            for record in self:
                if not re.match("^[a-zA-Z0-9_/\\\\]*$", record.code_profile):
                    raise ValidationError(_(
                        "Invalid Profile Code, please try again ( Profile Code only contains letters, numbers and character: / , \\ , _ ) ."))

    @api.one
    @api.constrains('release_time', 'bid_submission_deadline')
    def validate_release_time_bid_submission_deadline(self):
        if self.release_time and self.bid_submission_deadline:
            if self.release_time > self.bid_submission_deadline:
                raise ValidationError(_('Bid Submission Deadline cannot be set before Release Time !'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    invitation_pq_document_procurement_id = fields.Many2one('vnitpro.procurement', 'Invitation PQ Document Procurement',
                                                            ondelete='cascade')
