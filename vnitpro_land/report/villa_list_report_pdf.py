# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import api, _, models
from datetime import datetime
import time
import pytz
import logging
from odoo.addons.vnitpro_base.models.base import BaseInformation as base

_logger = logging.getLogger(__name__)


class ReportVillaList(models.AbstractModel):
    _name = "report.vnitpro_land.report_gen_villa_list"

    def get_count(self, data):
        villa_ids = self.env['vnitpro.land.use.rights'].browse(data['villa_id'])
        return len(villa_ids)

    def get_data(self, data):
        villa_ids = self.env['vnitpro.land.use.rights'].browse(data['villa_id'])
        list_villa = []
        count = 0
        for villa in villa_ids:
            count += 1
            if villa.address_number and villa.street and villa.ward_id:
                address = villa.address_number + ' / ' + villa.street + ' / ' + villa.ward_id.name + ' / ' + \
                          _(villa.district_id.name) + ' / ' + _(villa.city_id.name)
            if villa.land_group_id:
                villa_land_group = villa.land_group_id.name
            else:
                villa_land_group = ' '
            list_owner = []
            len_owner_detail = len(villa.owner_information_ids)
            for owner in villa.owner_information_ids:
                if owner.owner_phone:
                    owner_phone = owner.owner_phone
                else:
                    owner_phone = _('No Phone')

                if owner.have_certification == True:
                    have_certification = 1
                else:
                    have_certification = 0
                total_area_in_certification = base.check_number(self, owner.total_area_in_certification)
                private_own = base.check_number(self, owner.private_own)
                public_own = base.check_number(self, owner.public_own)
                if owner.own_time:
                    own_time = owner.own_time
                else:
                    own_time = ' '
                tz_current = pytz.timezone(self.env.user.partner_id.tz)  # get timezone user
                tz_database = pytz.timezone('UTC')
                if owner.certification_date:
                    certification_date = tz_database.localize(datetime.strptime(owner.certification_date, '%Y-%m-%d'))
                    certification_date = certification_date.astimezone(tz_current)
                    certification_date = certification_date.strftime(_('%m-%d-%Y'))
                owner_detail = {
                    'owner_information': owner.owner_name,
                    'owner_phone': owner_phone,
                    'total_area_in_certification': total_area_in_certification,
                    'certification_date': certification_date,
                    'have_certification': have_certification,
                    'private_own': private_own,
                    'public_own': public_own,
                    'own_time': own_time,
                }
                list_owner.append(owner_detail)
            land_area = base.check_number(self, villa.land_area)
            construction_area = base.check_number(self, villa.construction_area)
            details = {
                'count': count,
                'code': villa.code,
                'address': address,
                'villa_group': villa_land_group,
                'land_area': land_area,
                'construction_area': construction_area,
                'owner_detail': list_owner,
                'len_owner_detail': len_owner_detail,
            }
            list_villa.append(details)
        return list_villa

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        lang = self.env.user.partner_id.lang
        _logger.warning(lang)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'lang': lang,
            'get_count': self.get_count,
            'get_data': self.get_data,
        }
        return docargs
