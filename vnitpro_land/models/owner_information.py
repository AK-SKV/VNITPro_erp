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
import datetime
_logger = logging.getLogger(__name__)


class OwnerInformation(models.Model):
    _name = 'vnitpro.land.owner.information'
    _inherit = 'mail.thread'
    _rec_name = "owner_name"
    _order = 'land_id, have_certification desc, owner_name'
    _description = 'Owner'

    land_id = fields.Many2one('vnitpro.land.use.rights', 'Owner Of Land', ondelete="cascade", required=True)

    # Owener Information - Thông tin chủ sở hữu
    owner_name = fields.Char('Owner Name', size=150, required=True, track_visibility="onchange")
    owner_phone = fields.Char('Owner Phone', size=20, track_visibility="onchange")
    extra_owner_id = fields.One2many('vnitpro.land.extra.owner', 'owner_information_id', 'Extra Owner')
    have_certification = fields.Boolean('Have Certification ?', track_visibility="onchange")
    certification_date = fields.Date('Certification Date', track_visibility="onchange")
    using_area = fields.Float('Using Area', digits=(3, 2), track_visibility="onchange")

    # Area Information - Thông tin diện tích
    total_area_in_certification = fields.Float(
        'Total Area In Certification', digits=(3, 2), track_visibility="onchange")
    area = fields.Char('Area', size=255, track_visibility="onchange")
    rank = fields.Char('Rank', size=200, track_visibility="onchange")
    house_type = fields.Char('House Type', size=200, track_visibility="onchange")
    construction_area = fields.Float('Construction Area', digits=(3, 2), track_visibility="onchange")
    floor_area = fields.Float('Floor Area', digits=(3, 2), track_visibility="onchange")
    private_own = fields.Float('Private Own', digits=(3, 2), track_visibility="onchange")
    public_own = fields.Float('Public Own', digits=(3, 2), track_visibility="onchange")
    detail_information = fields.Html('Detail Information', size=1500, track_visibility="onchange")
    own_time = fields.Char('Own Time', size=255, track_visibility="onchange")

    # Attachment Files - Tệp tin đính kèm
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'land_owner_information_id', 'Attachment Files')

    def change_format_date(self, date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
        return date

    @api.multi
    @api.onchange('owner_name')
    def change_owner_name(self):
        if self.owner_name:
            self.have_certification = True

    @api.multi
    @api.constrains('construction_area', 'floor_area', 'private_own', 'public_own', 'total_area_in_certification')
    def constrains_area(self):
        for record in self:
            msg = ''
            if record.have_certification == True:
                if record.total_area_in_certification <= 0:
                    msg += _('Total area in certification cannot be set equal or lower than 0 \n')
                if record.construction_area < 0:
                    msg += _('Construction area cannot be set lower than 0 \n')
                if record.floor_area < 0:
                    msg += _('Floor area cannot be set lower than 0 \n')
                if record.private_own < 0:
                    msg += _('Garden area cannot be set lower than 0 \n')
                if record.public_own < 0:
                    msg += _('Total floor area to use cannot be set lower than 0')
            else:
                if record.using_area <= 0:
                    msg += _('Using area cannot be set equal or lower than 0 \n')

            if msg != '':
                raise ValidationError(msg)


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    land_owner_information_id = fields.Many2one('vnitpro.land.owner.information', 'Land Use Rights', ondelete='cascade')


class ExtraOwer(models.Model):
    _name = 'vnitpro.land.extra.owner'
    _inherit = 'mail.thread'
    _description = 'Extra Owner'
    _order = 'land_id, owner_information_id, name'

    owner_information_id = fields.Many2one(
        'vnitpro.land.owner.information', 'Extra Owner With', ondelete="cascade", required=True, track_visibility="onchange")
    land_id = fields.Many2one('vnitpro.land.use.rights', 'Land', related="owner_information_id.land_id", readonly=True)
    name = fields.Char('Name', size=150, required=True, track_visibility="onchange")
    note = fields.Text('Note', size=900, track_visibility="onchange")
