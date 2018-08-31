# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api
from odoo.tools import ustr
import unicodedata
import re


class SmsOnlineExamResult(models.Model):
    _name = 'sms.online.exam.result'

    name = fields.Char('Name', compute="compute_name")
    candidate_name = fields.Char('Candidate Name', size=120, required=True)
    candidate_birthday = fields.Date('Birthday', required=True)
    indentity_card = fields.Char('Identity Card', required=True, size=20)
    exam_id = fields.Many2one('sms.online.exam', 'Exam', required=True)
    unit_id = fields.Many2one('sms.online.exam.contestant', 'Unit', required=True)
    object_id = fields.Many2one('sms.online.exam.object', 'Position', required=True)
    start_exam_time = fields.Datetime('Start Exam Time', required=True)
    end_exam_time = fields.Datetime('Start Exam Time', required=True)
    point = fields.Float('Point', digits=(3, 2), required=True)
    token = fields.Char(string="Token")
    state = fields.Selection([('incomplete', 'Incomplete'), ('complete', 'Complete')], string="State")
    result = fields.Boolean('Passed?', compute="compute_result", store=True)

    @api.multi
    @api.depends('exam_id', 'point')
    def compute_result(self):
        for record in self:
            if record.exam_id and record.exam_id.passing_point <= record.point:
                record.result = True
            else:
                record.result = False

    @api.multi
    @api.depends('candidate_name', 'exam_id')
    def compute_name(self):
        for record in self:
            if record.candidate_name and record.exam_id:
                record.name = record.candidate_name + ' - ' + record.exam_id.name
            else:
                record.name = ''
