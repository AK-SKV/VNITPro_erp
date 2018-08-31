# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _

RESULT = [(1, 'Passed'), (2, 'Not Passed')]


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    confirm_pre_ids = fields.One2many('vnitpro.confirm.prequalification',
                                      'procurement_id', 'Comfirm Prequalification List')
    finished_to_comfirm_prequalification = fields.Boolean('Finished To Comfirm Prequalification')


class ConfirmPrequalification(models.Model):
    _name = "vnitpro.confirm.prequalification"

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', required=True, ondelete="cascade")
    approve_pq_document_id = fields.Many2one('vnitpro.approve.pq.document', 'Select The Pre-Selection', required=True)
    expertise_team_leader = fields.Many2one('vnitpro.employee', 'Expertise Team Leader',
                                            domain="[('activate','=','usage')]", required=True)
    expertise_team_member = fields.Many2one('vnitpro.employee', 'Expertise Team Member',
                                            domain="[('activate','=','usage')]", required=True)
    expert_team_leader = fields.Many2one('vnitpro.employee', 'Expert Team Leader', domain="[('activate','=','usage')]",
                                         required=True)
    expert_team_member = fields.Many2one('vnitpro.employee', 'Expert Team Member', domain="[('activate','=','usage')]",
                                         required=True)
    bid_submission_deadline = fields.Date('Evaluation Date', track_visibility="onchange", required=True)
    review_and_note = fields.Text('Review And Note', size=200)
    result = fields.Selection(RESULT, 'Result', required=True, default=1)
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'confirm_pre_id', 'Attach Files')

    _sql_constraints = [('uni_procurement_pq_document',
                         'unique(procurement_id,approve_pq_document_id)',
                         'Performance qualification document must be unique per Approve PQ Document List')]


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    confirm_pre_id = fields.Many2one('vnitpro.confirm.prequalification',
                                     'Confirm Prequalification List', ondelete='cascade')
