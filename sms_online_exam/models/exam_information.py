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


class SmsOnlineExam(models.Model):
    _name = 'sms.online.exam'
    _inherit = 'vnitpro.base.information'

    object_id = fields.Many2one('sms.online.exam.object', 'Object', required=True)
    councilman = fields.Char('Councilman', size=200, required=True)
    exam_council = fields.Char('Exam Council', size=200, required=True)
    duration = fields.Integer('Duration', required=True, size=3)
    number_questions = fields.Integer('Number Questions', size=3, required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    passing_point = fields.Float('Passing Point', digits=(3, 2), required=True)
    process_list = fields.One2many('sms.online.exam.process.list', 'online_exam_id', 'Process List')
    code = fields.Char(required=False)
    slug = fields.Char(string="Slug", compute="slug_name", store="True")

    @api.multi
    @api.depends('name')
    def slug_name(self):
        for record in self:
            if record.name:
                s = ustr(record.name)
                uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
                slug = re.sub('[\W_]', ' ', uni).strip().lower()
                slug = re.sub('[-\s]+', '-', slug)
                record.slug = slug


class SmsOnlineExamProcessList(models.Model):
    _name = 'sms.online.exam.process.list'

    online_exam_id = fields.Many2one('sms.online.exam', 'Online Exam', required=True, ondelete="cascade")
    process_id = fields.Many2one('sms.online.exam.process', 'Process', required=True)
    number_questions = fields.Integer('Number Questions', size=3)
