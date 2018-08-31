# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Created by: tam.pt
###############################################################################

from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)


class BaseAttachment(models.Model):
    _inherit = 'vnitpro.base.attachment'

    project_id = fields.Many2one('vnitpro.project', 'Attachment', required=True, ondelete="cascade")
    confirm_project_id = fields.Many2one('vnitpro.project', 'Attachment', required=True, ondelete='cascade')
