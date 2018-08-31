# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api, _
from lxml import etree
import logging
_logger = logging.getLogger(__name__)
STATUS = [('usage', 'Usage'), ('notused', 'Not used')]


class Test(models.Model):
    _name = "vnitpro.test"

    name = fields.Char('Name', size=255, required=True)
    attachment_ids = fields.One2many('vnitpro.test.attachment', 'test_id', 'Attachment files')
    permission_ids = fields.One2many('vnitpro.test.permission', 'test_id')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        _logger.warning(view_type)
        res = super(Test, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        # if self._context.get('type'):
        doc = etree.XML(res['arch'])
        if view_type == 'form' and 1 == 1:
            for node in doc.xpath("//form"):
                node.set('create', 'false')
                node.set('delete', 'false')
        res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
