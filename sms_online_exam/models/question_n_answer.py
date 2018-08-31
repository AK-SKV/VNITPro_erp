# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class SmsOnlineExamQuestion(models.Model):
    _name = 'sms.online.exam.question'
    _order = 'activate,process_id,object_id'

    name = fields.Char('Name', compute="_compute_name")
    question_content = fields.Html('Question Content', required=True)
    anwser_ids = fields.One2many('sms.online.exam.answer', 'question_id', 'List Answer')
    process_id = fields.Many2one('sms.online.exam.process', 'Process', required=True)
    object_id = fields.Many2one('sms.online.exam.object', 'Object', required=True)
    activate = fields.Selection([('usage', 'Usage'), ('not_used', 'Not Used')],
                                'Status', default="usage", required=True)

    @api.multi
    @api.depends('process_id', 'object_id')
    def _compute_name(self):
        for record in self:
            if record.process_id and record.object_id and record.id:
                record.name = record.process_id.name + ' - ' + \
                    record.object_id.name + _(' - Question ') + str(record.id)
            else:
                record.name = ''


class SmsOnlineExamAnswer(models.Model):
    _name = 'sms.online.exam.answer'

    question_id = fields.Many2one('sms.online.exam.question', 'Question', required=True, ondelete="cascade")
    answer_content = fields.Text('Answer Content', required=True)
    true_false = fields.Boolean('True/False')
