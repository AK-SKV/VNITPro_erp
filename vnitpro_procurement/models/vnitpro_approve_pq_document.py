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

    approve_pq_document_ids = fields.One2many('vnitpro.approve.pq.document', 'procurement_id', 'List PQ Document')

    # procurement state
    finished_to_approve_pq_document = fields.Boolean('Finished To Approve PQ Document')


class ApprovePQDocument(models.Model):
    _name = "vnitpro.approve.pq.document"

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', ondelete='cascade', required=True)
    code = fields.Char('Profile Code', size=50, track_visibility="onchange", required=True)
    name = fields.Char('Profile Name', size=300, track_visibility="onchange", required=True)
    bidder_id = fields.Many2one('vnitpro.bidder', 'Bidder', track_visibility="onchange",
                                required=True, domain="[('activate','=', 'usage'),('activate','=','usage')]")
    document_submission_date = fields.Date('Document Submission Date', track_visibility="onchange", required=True)
    submission_name = fields.Char('Submission Name', size=300, track_visibility="onchange", required=True)
    contact_information = fields.Text('Contact Information', size=300, track_visibility="onchange", required=True)
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'approve_pq_document_id', 'Attach Files')

    _sql_constraints = [('unique_code_procurment_id', 'unique(code,procurement_id)', 'Code Profile already exits!'),
                        ('unique_bidder_id_procurement_id', 'unique(bidder_id,procurement_id)', 'Bidder must be unique per PQ document list')]

    @api.multi
    @api.constrains('code')
    def _compute_special_character_code(self):
        if self.code:
            for record in self:
                if not re.match("^[a-zA-Z0-9_/\\\\]*$", record.code):
                    raise ValidationError(_(
                        "Invalid Profile Code, please try again ( Profile Code only contains letters, numbers and character: / , \\ , _ ) ."))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    approve_pq_document_id = fields.Many2one('vnitpro.approve.pq.document', 'Approve PQ Document', ondelete='cascade')
