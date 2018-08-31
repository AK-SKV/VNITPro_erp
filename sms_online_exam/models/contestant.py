# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api


class SmsOnlineExamContestant(models.Model):
    _name = 'sms.online.exam.contestant'
    _inherit = 'vnitpro.base.information'
