# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api, _


class TestAttachment(models.Model):
    _name = "vnitpro.test.attachment"
    _inherit = "vnitpro.base.attachment"

    test_id = fields.Many2one('vnitpro.test', 'Test', required=True, ondelete='cascade')
