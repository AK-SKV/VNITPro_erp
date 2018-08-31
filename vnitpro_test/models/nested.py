# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class TestNested(models.Model):
    _name = "vnitpro.test.nested"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'name'
    _order = 'parent_left'

    stt = fields.Char('STT', required=False, compute='_compute_stt')
    code = fields.Char('code', required=False, )
    name = fields.Char('name', required=False, )
    parent_id = fields.Many2one('vnitpro.test.nested', 'Parent Nested', index=True, ondelete='cascade')
    child_id = fields.One2many('vnitpro.test.nested', 'parent_id', 'Child Nested')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)

    @api.one
    def _compute_stt(self):
        if self.parent_id:
            self.stt = '|' + str('_' * 2) + self.parent_id.stt.replace('|', '')
        else:
            self.stt = ''
