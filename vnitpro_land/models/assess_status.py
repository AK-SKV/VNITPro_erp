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


class ProcessUnit(models.Model):
    _name = "vnitpro.process.unit"
    _inherit = "vnitpro.base.information", "mail.thread"
    _description = "Process Unit"


class AssessStatus(models.Model):
    _name = "vnitpro.assess.status"
    _description = 'Assess Status'
    _rec_name = "profile_name"
    _order = "land_id"

    land_id = fields.Many2one('vnitpro.land.use.rights', 'Land', ondelete="cascade",
                              required=True,  domain="[('activate','=','usage')]", track_visibility="onchange")  # Khu đất
    profile_name = fields.Char('Profile Name', size=255, required=True, track_visibility="onchange")  # Tên hồ sơ
    process_unit = fields.Many2one('vnitpro.process.unit', 'Process Unit', required=True,
                                   domain="[('activate','=','usage')]", track_visibility="onchange")  # Đơn vị thực hiện
    create_profile_date = fields.Date('Create Profile Date', default=fields.Date.today(),
                                      required=True, track_visibility="onchange")  # ngày tạo hồ sơ
    assess_status_detail_ids = fields.One2many(
        'vnitpro.assess.status.detail', 'assess_status_id', 'Assess Status Detail')  # Bảng chi tiết đánh giá hiện trạng

    # Attachment - Đính kèm tệp tin
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'assess_status_id', 'Attachment Files')

    def view_detail_assess_status(self):
        view_id = self.env.ref('vnitpro_land.view_vnitpro_assess_status_form', False)
        return {
            'name': _('Assess Status'),
            'domain': [],
            'res_model': 'vnitpro.assess.status',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': {},
            'views': [(view_id.id, 'form')],
            'view_id': view_id.id,
        }


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    assess_status_id = fields.Many2one('vnitpro.assess.status', 'Assess Status', ondelete='cascade')
