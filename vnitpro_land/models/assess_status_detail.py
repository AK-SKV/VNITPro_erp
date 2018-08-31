# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


class AssessStatusDetail(models.Model):
    _name = "vnitpro.assess.status.detail"
    _description = 'Assess Status Detail'
    _inherit = "mail.thread"

    assess_status_id = fields.Many2one('vnitpro.assess.status', 'Assess Status',
                                       required=True, ondelete="cascade", track_visibility="onchange")
    area = fields.Char('Area', size=200, required=True, track_visibility="onchange")
    assess_category_id = fields.Many2one('vnitpro.assess.category', 'Assess Category',
                                         required=True, domain="[('activate','=','usage')]", track_visibility="onchange")
    content_detail = fields.Text('Content Detail', size=1000, required=True, track_visibility="onchange")
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'assess_status_detail_id', 'Attachment Files')


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    assess_status_detail_id = fields.Many2one('vnitpro.assess.status.detail',
                                              'Assess Status Detail', ondelete='cascade')
