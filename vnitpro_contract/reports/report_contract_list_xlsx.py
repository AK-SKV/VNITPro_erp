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


class ReportContractListXlsx(models.AbstractModel):
    _name = 'report.vnitpro_contract.report_gen_contract_list_xlsx'
    _inherit = 'report.vnitpro_contract.report_gen_contract_list', 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10})
        italic = workbook.add_format({'italic': True})
        title_line_format = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'})
        date_line_format = workbook.add_format(
            {'italic': True, 'font_size': 14, 'align': 'center', 'bold': True, 'valign': 'vcenter'})
        date_format = workbook.add_format({'num_format': _('dd-mm-yyyy')})
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
        data_contract = partners.count_contract_ids()
        row += 1
        col = 0
        data_table = self.get_data(data_contract)
        for data in data_table:
            sheet.write(row, col, data['name'])
            sheet.write(row, col + 1, data['code'])
            sheet.write(row, col + 2, data['bidder_a'])
            sheet.write(row, col + 3, data['bidder_b'])
            sheet.write(row, col + 4, data['contract_cost'])
            sheet.write(row, col + 5, data['currency'])
            sheet.write(row, col + 6, data['contract_creator'])
            sheet.write(row, col + 7, data['contract_create_date'])
            sheet.write(row, col + 8, data['status'])
            sheet.write(row, col + 9, data['contract_type_id'])
            row += 1
