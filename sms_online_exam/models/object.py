# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api


class SmsOnlineExamObject(models.Model):
    _name = 'sms.online.exam.object'
    _inherit = 'vnitpro.base.information'
