# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, _
from datetime import datetime
import time
import pytz
import logging
import xlsxwriter

_logger = logging.getLogger(__name__)


class ReportProcurementListXlsx(models.AbstractModel):
    _name = 'report.vnitpro_procurement.report_gen_procurement_list_xlsx'
    _inherit = 'report.vnitpro_procurement.report_gen_procurement_list', 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet(_('Procurement List'))
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10})
        italic = workbook.add_format({'italic': True})
        title_line_format = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'})
        date_line_format = workbook.add_format(
            {'italic': True, 'font_size': 14, 'align': 'center', 'bold': True, 'valign': 'vcenter'})
        date_format = workbook.add_format({'num_format': _('mm-dd-yyyy')})
        sheet.set_column('A:M', 18)
        row = 0
        col = 0

        # Tiêu đề báo cáo
        data_title = self.get_title_report()
        row += 5
        sheet.merge_range('A1:M3', data_title['title_report'], title_line_format)
        sheet.merge_range('A4:M5', data_title['time_report'], date_line_format)

        # Tiêu đề bảng báo cáo
        row += 1
        data_title_table = self.get_title_table()
        for data_title in data_title_table:
            sheet.write(row, col, data_title, bold_center)
            col += 1

        # Dữ liệu bảng báo cáo
        data_procuremnt = partners.count_procurement_ids()
        row += 1
        col = 0
        data_table = self.get_data(data_procuremnt)
        for data in data_table:
            sheet.write(row, col, data['code'])
            sheet.write(row, col + 1, data['name'])
            sheet.write(row, col + 2, data['time_bidder_select'])
            sheet.write(row, col + 3, data['time_contract_duration'])
            sheet.write(row, col + 4, data['funds'])
            sheet.write(row, col + 5, data['time_invitation'])
            sheet.write(row, col + 6, data['time_bidding'])
            sheet.write(row, col + 7, data['date_open_file'])
            sheet.write(row, col + 8, data['time_review'])
            sheet.write(row, col + 9, data['new_history'])
            sheet.write(row, col + 10, data['bidder_won'])
            sheet.write(row, col + 11, data['value_procurement'])
            sheet.write(row, col + 12, data['value_won'])
            sheet.write(row, col + 13, data['currency'])
            row += 1
