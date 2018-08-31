# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, api, _
from odoo.addons.vnitpro_base.models.base import BaseInformation as base
import datetime
import locale
import logging
_logger = logging.getLogger(__name__)


class ReportVillaListXlsx(models.AbstractModel):
    _name = 'report.vnitpro_land.report_villa_list_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        title_company = workbook.add_format(
            {'bold': True, 'font_size': 9, 'valign': 'vcenter', 'align': 'center', 'font_name': 'Times New Roman'})
        title_report = workbook.add_format(
            {'bold': True, 'font_size': 12, 'valign': 'vcenter', 'align': 'center', 'font_name': 'Times New Roman'})
        title_numbered = workbook.add_format(
            {'bold': True, 'font_size': 9, 'valign': 'vcenter', 'align': 'left', 'font_name': 'Times New Roman'})

        bold_title_center = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center',
                                                 'font_size': 9, 'valign': 'vcenter', 'font_name': 'Times New Roman', 'border': 1})
        numberic = workbook.add_format({'align': 'right', 'font_size': 9, 'text_wrap': True,
                                        'valign': 'vcenter', 'font_name': 'Times New Roman', 'border': 1})
        string_content_table = workbook.add_format({'align': 'left', 'font_size': 9, 'text_wrap': True,
                                                    'valign': 'vcenter', 'font_name': 'Times New Roman', 'border': 1})
        string_content_table_center = workbook.add_format({'align': 'center', 'font_size': 11, 'italic': True, 'text_wrap': True,
                                                           'valign': 'vcenter', 'font_name': 'Times New Roman', 'border': 1})
        id_format = workbook.add_format({'align': 'center', 'font_size': 9,
                                         'valign': 'vcenter', 'font_name': 'Times New Roman', 'border': 1})
        date_format = workbook.add_format({'num_format': _('d mmmm yyyy'), 'valign': 'vcenter', 'text_wrap': True,
                                           'font_name': 'Times New Roman', 'border': 1, 'font_size': 9, })

        domain = [('activate', '=', 'usage')]
        if partners.land_type:
            domain.append(('land_type', '=', partners.land_type))
        if partners.land_group_id:
            domain.append(('land_group_id', '=', partners.land_group_id.id))
        if partners.ward_id:
            domain.append(('ward_id', '=', partners.ward_id.id))
        _logger.warning(domain)
        villa_ids = self.env['vnitpro.land.use.rights'].search(domain, order="ward_id, name")
        _logger.warning(villa_ids)
        sheet.set_column('A:A', 4)
        sheet.set_column('B:B', 12)
        sheet.set_column('C:C', 26)
        sheet.set_column('D:D', 13)
        sheet.set_column('E:F', 13)
        sheet.set_column('G:G', 19)
        sheet.set_column('H:H', 13)
        sheet.set_column('I:L', 13)
        sheet.set_column('M:M', 14)

        sheet.merge_range('A1:C1', _("People's Committee of Ha Noi city"), title_company)
        sheet.merge_range('A2:C2', _("Hai Ba Trung District"), title_company)
        if partners.ward_id:
            sheet.merge_range('E1:I2', _("Current Condition Of Villa Using Report - %s") %
                              partners.ward_id.name, title_report)
        else:
            sheet.merge_range('E1:I2', _("Current Condition Of Villa Using Report"), title_report)
        sheet.merge_range('K1:L2', _("Numbered:"), title_numbered)
        sheet.merge_range('B4:C4', _("Villa Quantity: %d") % len(villa_ids),
                          workbook.add_format({'font_size': 9, 'align': 'center'}))
        sheet.merge_range('A6:A8', _("#"), bold_title_center)
        sheet.merge_range('B6:B8', _("Villa Code"), bold_title_center)
        sheet.merge_range('C6:C8', _("Address"), bold_title_center)
        sheet.merge_range('D6:D8', _("Villa Group"), bold_title_center)
        sheet.merge_range('E6:E8', _("Land Area"), bold_title_center)
        sheet.merge_range('F6:F8', _("Construction Area"), bold_title_center)
        sheet.merge_range('G6:G8', _("Owner Information"), bold_title_center)
        sheet.merge_range('H6:H8', _("Owner Phone"), bold_title_center)
        sheet.merge_range('I6:I8', _("Own Area/ Area in Certificate"), bold_title_center)
        sheet.merge_range('K6:M6', _("Using Status"), bold_title_center)
        sheet.merge_range('J6:J8', _("Certification Date"), bold_title_center)

        sheet.merge_range('K7:K8', _("Private Own"), bold_title_center)
        sheet.merge_range('L7:L8', _("Public Own"), bold_title_center)
        sheet.merge_range('M7:M8', _("Own Time"), bold_title_center)

        if len(villa_ids) > 0:
            i = 1
            row = 8
            for villa_id in villa_ids:
                m = 0
                n = 0
                len_owner = len(villa_id.owner_information_ids)
                # Address String - Chuỗi địa chỉ
                address = ''
                if villa_id.address_number and villa_id.street and villa_id.ward_id:
                    address = villa_id.address_number + ' / ' + villa_id.street + ' / ' + villa_id.ward_id.name + ' / ' + \
                        _(villa_id.district_id.name) + ' / ' + _(villa_id.city_id.name)
                row += 1
                if len_owner > 1:
                    while m < len_owner:
                        # sheet.set_row(row + m - 1, 25)
                        m += 1
                    for owner_id in villa_id.owner_information_ids:
                        # Owner Name - Chủ sở hữu
                        sheet.write('G{}'.format(row + n),
                                    owner_id.owner_name if owner_id.owner_name else '', string_content_table)
                        sheet.write('H{}'.format(row + n),
                                    owner_id.owner_phone if owner_id.owner_phone else _('No'), string_content_table)
                        if owner_id.have_certification == True:
                            # Own Area/Area in Certificate
                            sheet.write('I{}'.format(row + n), base.check_number(self, owner_id.total_area_in_certification)
                                        if owner_id.total_area_in_certification > 0 else 0, numberic)
                            # Certificate Date - Ngày cấp sổ đỏ
                            try:
                                if owner_id.certification_date:
                                    certification_date = datetime.datetime.strptime(
                                        owner_id.certification_date, '%Y-%m-%d')
                            except:
                                certification_date = ''
                            sheet.write_datetime('J{}'.format(row + n), certification_date, date_format)
                            # Private Own - Sở hữu riêng
                            sheet.write('K{}'.format(row + n), base.check_number(self, owner_id.private_own)
                                        if owner_id.private_own > 0 else 0, string_content_table)
                            # Public Own - Sở hữu chung
                            sheet.write('L{}'.format(row + n), base.check_number(self, owner_id.public_own)
                                        if owner_id.public_own > 0 else 0, string_content_table)
                            # Own Time - Thời gian sở hữu
                            sheet.write('M{}'.format(row + n), owner_id.own_time if owner_id.own_time else '',
                                        string_content_table)
                        else:
                            # Own Area/Area in Certificate
                            sheet.write('I{}'.format(row + n), base.check_number(self, owner_id.using_area)
                                        if owner_id.using_area > 0 else 0, numberic)
                            sheet.merge_range('J{}:M{}'.format(row + n, row + n), _('The owner have no certification'),
                                              string_content_table_center)
                        n += 1
                    # ID - STT
                    sheet.merge_range('A{}:A{}'.format(row, row + len_owner - 1), i, id_format)
                    # Villa Code - Mã biệt thự
                    sheet.merge_range('B{}:B{}'.format(row, row + len_owner - 1),
                                      villa_id.code if villa_id.code else '', string_content_table)
                    # Address - Địa chỉ
                    sheet.merge_range('C{}:C{}'.format(row, row + len_owner - 1), address, string_content_table)
                    # Land Group - Nhóm
                    sheet.merge_range('D{}:D{}'.format(row, row + len_owner - 1),
                                      villa_id.land_group_id.name if villa_id.land_group_id.name else '', string_content_table)
                    # Land Area - Diện tích khu đất
                    sheet.merge_range('E{}:E{}'.format(row, row + len_owner - 1),
                                      base.check_number(self, villa_id.land_area), numberic)
                    # Construction Area - Diện tích xây dựng
                    sheet.merge_range('F{}:F{}'.format(row, row + len_owner - 1),
                                      base.check_number(self, villa_id.construction_area), numberic)
                    row += len_owner - 1
                else:
                    # sheet.set_row(row - 1, 25)
                    # ID - STT
                    sheet.write('A{}'.format(row), i, id_format)
                    # Villa Code - Mã biệt thự
                    sheet.write('B{}'.format(row), villa_id.code if villa_id.code else '', string_content_table)
                    # Address - Địa chỉ
                    sheet.write('C{}'.format(row), address, string_content_table)
                    # Land Group - Nhóm
                    sheet.write('D{}'.format(row),
                                villa_id.land_group_id.name if villa_id.land_group_id.name else '', string_content_table)
                    # Land Area - Diện tích khu đất
                    sheet.write('E{}'.format(row), base.check_number(self, villa_id.land_area), numberic)
                    # Construction Area - Diện tích xây dựng
                    sheet.write('F{}'.format(row), base.check_number(self, villa_id.construction_area), numberic)
                    if len_owner > 0:
                        # Owner Name - Chủ sở hữu
                        sheet.write('G{}'.format(row),
                                    villa_id.owner_information_ids.owner_name if villa_id.owner_information_ids.owner_name else '', string_content_table)
                        sheet.write('H{}'.format(row),
                                    villa_id.owner_information_ids.owner_phone if villa_id.owner_information_ids.owner_phone else _('No'), string_content_table)
                        if villa_id.owner_information_ids.have_certification == True:
                            # Own Area/Area in Certificate
                            sheet.write('I{}'.format(row), base.check_number(self, villa_id.owner_information_ids.total_area_in_certification)
                                        if villa_id.owner_information_ids.total_area_in_certification > 0 else 0, numberic)
                            # Certificate Date - Ngày cấp sổ đỏ
                            try:
                                if villa_id.owner_information_ids.certification_date:
                                    certification_date = datetime.datetime.strptime(
                                        villa_id.owner_information_ids.certification_date, '%Y-%m-%d')
                            except:
                                certification_date = ''
                            sheet.write_datetime('J{}'.format(row), certification_date, date_format)
                            # Private Own - Sở hữu riêng
                            sheet.write('K{}'.format(row), base.check_number(self, villa_id.owner_information_ids.private_own)
                                        if villa_id.owner_information_ids.private_own > 0 else 0, string_content_table)
                            # Public Own - Sở hữu chung
                            sheet.write('L{}'.format(row), base.check_number(self, villa_id.owner_information_ids.public_own)
                                        if villa_id.owner_information_ids.public_own > 0 else 0, string_content_table)
                            # Own Time - Thời gian sở hữu
                            sheet.write('M{}'.format(row), villa_id.owner_information_ids.own_time if villa_id.owner_information_ids.own_time else '',
                                        string_content_table)
                        else:
                            # Own Area/Area in Certificate
                            sheet.write('I{}'.format(row), base.check_number(self, villa_id.owner_information_ids.using_area)
                                        if villa_id.owner_information_ids.using_area > 0 else 0, numberic)
                            sheet.merge_range('J{}:M{}'.format(row, row), _('The owner have no certification'),
                                              string_content_table_center)
                    else:
                        sheet.merge_range('G{}:M{}'.format(row, row), _('Have no owner'), string_content_table_center)
                i += 1

            string_content_title = workbook.add_format({'align': 'center', 'font_size': 9, 'bold': True,
                                                        'valign': 'vcenter', 'font_name': 'Times New Roman'})
            row += 2
            sheet.merge_range('C{}:E{}'.format(row, row), _('Create User'), string_content_title)
            sheet.merge_range('I{}:K{}'.format(row, row), _('Unit Manager'), string_content_title)

            string_content_sign = workbook.add_format({'align': 'center', 'font_size': 9, 'italic': True,
                                                       'valign': 'vcenter', 'font_name': 'Times New Roman'})
            row += 1
            sheet.merge_range('C{}:E{}'.format(row, row), _('( Sign And Write Fullname )'), string_content_sign)
            sheet.merge_range('I{}:K{}'.format(row, row), _('( Sign And Write Fullname )'), string_content_sign)
        else:
            sheet.merge_range('A9:M9', _('Have No Information Of Villa.'), string_content_table_center)
