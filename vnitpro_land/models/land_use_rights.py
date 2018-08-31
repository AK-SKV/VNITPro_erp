# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
import re
import logging
_logger = logging.getLogger(__name__)

LAND_TYPE = [
    ('1st_grade_house', '1st Grade House'),
    ('2nd_grade_house', '2nd Grade House'),
    ('3th_grade_house', '3th Grade House'),
    ('4th_grade_house', '4th Grade House'),
    ('apartment', 'Apartment'),
    ('villa', 'Villa'),
]


class LandUseRights(models.Model):
    _name = 'vnitpro.land.use.rights'
    _inherit = 'vnitpro.base.information', 'mail.thread'
    _description = 'Land Use Rights'
    _order = 'activate, city_id, district_id, ward_id'

    avatar = fields.Binary('Avatar', attachment=True, track_visibility="onchange")
    survey_date = fields.Date('Survey Date', track_visibility="onchange")
    create_record_date = fields.Date(
        'Create Date', default=lambda self: fields.Date.today(), track_visibility="onchange")

    # General Information - Thông tin chung
    land_type = fields.Selection(LAND_TYPE, 'Land Type', default="villa", track_visibility="onchange")  # Loại khu đất
    land_group_id = fields.Many2one('vnitpro.land.group', 'Land Group',
                                    domain="[('activate','=','usage')]", track_visibility="onchange")  # Nhóm khu đất

    increase_reason = fields.Char('Increase Reason', size=255, track_visibility="onchange")  # Lý do tăng
    land_plots_number = fields.Char('Land Plots Number', size=120, track_visibility="onchange")  # Số thửa đất
    map_number = fields.Char('Map Number', size=120, track_visibility="onchange")  # Số tờ bản đồ
    certificate_book_number = fields.Char('Certificate Book Number', size=60,
                                          track_visibility="onchange")  # Số vào sổ GCN
    date_of_certification = fields.Date('Date Of Certification', track_visibility="onchange")  # Ngày cấp
    construction_year = fields.Char('Construction Year', size=200, track_visibility="onchange",
                                    default="Được xây dựng trước năm 1954")  # Ngày bắt đầu sử dụng

    # Address - Địa chỉ
    address_number = fields.Char('Address Number', size=255, required=True, track_visibility="onchange")
    street = fields.Char('Street Number', size=255, required=True, track_visibility="onchange")
    city_id = fields.Many2one('vnitpro.res.city', 'City', default=lambda self: self.env.ref(
        'vnitpro_base.vietnam_city_ha_noi', False), required=True, track_visibility="onchange")
    district_id = fields.Many2one('vnitpro.res.district', 'District', default=lambda self: self.env.ref(
        'vnitpro_base.vietnam_district_hai_ba_trung_hn', False), required=True, track_visibility="onchange")
    ward_id = fields.Many2one('vnitpro.res.ward', 'Ward', required=True, track_visibility="onchange")

    # Area Information - Thông tin diện tích khu đất
    land_area = fields.Float('Land Area', digits=(3, 2), track_visibility="onchange",
                             required=True)  # Diện tích khu đất
    land_limit = fields.Char('Land Limit', size=200, track_visibility="onchange")  # Giới hạn khu đất
    construction_area = fields.Float('Construction Area', digits=(
        3, 2), track_visibility="onchange")  # Diện tích xây dựng
    floor_number = fields.Integer('Floor Number', size=3, track_visibility="onchange")  # Số tầng
    garden_area = fields.Float('Garden Area', digits=(3, 2), track_visibility="onchange")  # Diện tích sân vườn
    total_floor_area_to_use = fields.Float(
        'Total Floor Area To Use', digits=(3, 2), track_visibility="onchange")  # Tổng diện tích sàn sử dụng
    purpose_of_use_id = fields.Many2one('vnitpro.purpose.of.use', 'Purpose Of Use',
                                        domain="[('activate','=', 'usage')]", track_visibility="onchange")  # Mục đích sử dụng
    usage_duration_id = fields.Many2one('vnitpro.land.usage.duration', 'Usage Duration',
                                        track_visibility="onchange", domain="[('activate','=','usage')]")  # Thời gian sử dụng
    usage_origin_id = fields.Many2one('vnitpro.land.usage.origin', 'Usage Origin',
                                      track_visibility="onchange", domain="[('activate','=','usage')]")  # Nguồn gốc sử dụng

    # Assess Status - Đánh giá tình trạng
    assess_status_ids = fields.One2many('vnitpro.assess.status', 'land_id', 'Assess Status')

    # Owner Information - Thông tin chủ sở hữu
    owner_information_ids = fields.One2many(
        'vnitpro.land.owner.information', 'land_id', 'Owner Information')

    # Attachment Files - Đính kèm tệp tin
    description_image = fields.Html('Description Image', track_visibility="onchange")
    attachment_ids = fields.One2many('vnitpro.base.attachment',
                                     'land_use_rights_id', 'Attachment Files')

    def change_format_date(self, date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
        return date

    @api.multi
    @api.constrains('land_area', 'construction_area', 'garden_area', 'floor_number', 'total_floor_area_to_use')
    def constrains_area(self):
        for record in self:
            msg = ''
            if record.land_area <= 0:
                msg += _('Land area cannot be set equal or lower than 0 \n')
            if record.construction_area < 0:
                msg += _('Construction area cannot be set lower than 0 \n')
            if record.floor_number < 0:
                msg += _('Floor number cannot be set lower than 0 \n')
            if record.garden_area < 0:
                msg += _('Garden area cannot be set lower than 0 \n')
            if record.total_floor_area_to_use < 0:
                msg += _('Total floor area to use cannot be set lower than 0')
            if msg != '':
                raise ValidationError(msg)


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    land_use_rights_id = fields.Many2one(
        'vnitpro.land.use.rights', 'Land Use Rights', ondelete='cascade')
