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
    _name = 'report.vnitpro_contract.report_gen_contract_list_detail_xlsx'
    _inherit = 'report.vnitpro_contract.report_gen_contract_list_detail', 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10})
        bold_title_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14})
        italic = workbook.add_format({'italic': True})
        title_line_format = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'})
        date_line_format = workbook.add_format(
            {'italic': True, 'font_size': 14, 'align': 'center', 'bold': True, 'valign': 'vcenter'})
        date_format = workbook.add_format({'num_format': _('dd-mm-yyyy')})
        sheet.set_column('A:I', 15)
        row = 0
        col = 0

        # Tiêu đề báo cáo
        data_title = self.get_title_report()
        row += 5
        sheet.merge_range('A1:I3', data_title['title_report'], title_line_format)
        sheet.merge_range('A4:I5', data_title['time_report'], date_line_format)

        data_contract_id = {}
        data_contract_id.update({'contract_id': partners.id})
        # Thông tin hợp đồng
        row += 1
        data_contract = self.get_data_contract(data_contract_id)
        for contract in data_contract:
            sheet.merge_range('A{}:B{}'.format(row, row), contract[0], bold)
            sheet.merge_range('C{}:I{}'.format(row, row), contract[1])
            row += 1

        # guarantee: bao lanh
        row += 1
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_guarantee()
                          ['title_guarantee'], bold_title_center)
        row += 1
        title_table_guarantee = self.get_title_table_guarantee()
        for title in title_table_guarantee:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_guarantee = self.get_data_guarantee(data_contract_id)
        for guarantee in data_guarantee:
            sheet.write(row, col, guarantee['guarantee_type'])
            sheet.write(row, col + 1, guarantee['guarantee_unit'])
            sheet.write(row, col + 2, guarantee['status'])
            sheet.write(row, col + 3, guarantee['create_date'])
            sheet.write(row, col + 4, guarantee['start_date'])
            sheet.write(row, col + 5, guarantee['end_date'])
            sheet.write(row, col + 6, guarantee['price'])
            sheet.write(row, col + 7, guarantee['note'])
            row += 1

        # category: hang muc hop dong
        row += 1
        col = 0
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_category()['title_category'],
                          bold_title_center)
        row += 1
        title_table_category = self.get_title_table_category()
        for title in title_table_category:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_category = self.get_data_category(data_contract_id)
        for category in data_category:
            sheet.write(row, col, category['code_number'])
            sheet.write(row, col + 1, category['category'])
            sheet.write(row, col + 2, category['quantity'])
            sheet.write(row, col + 3, category['unit_price'])
            sheet.write(row, col + 4, category['vat'])
            sheet.write(row, col + 5, category['cost_after_vat'])
            sheet.write(row, col + 6, category['warranty_period'])
            sheet.write(row, col + 7, category['employee'])
            row += 1

        # Payment Term: dieu khoan thanh toan
        row += 1
        col = 0
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_payment_term()['title_payment_term'],
                          bold_title_center)
        row += 1
        title_table_payment_term = self.get_title_table_payment_term()
        for title in title_table_payment_term:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_payment_term = self.get_data_payment_term(data_contract_id)
        for payment_term in data_payment_term:
            sheet.write(row, col, payment_term['payment_name'])
            sheet.write(row, col + 1, payment_term['start_date'])
            sheet.write(row, col + 2, payment_term['end_date'])
            sheet.write(row, col + 3, payment_term['payment_price'])
            sheet.write(row, col + 4, payment_term['description'])
            row += 1

        # Sub: phu luc
        row += 1
        col = 0
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_sub()['title_sub'],
                          bold_title_center)
        row += 1
        title_table_sub = self.get_title_table_sub()
        for title in title_table_sub:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_sub = self.get_data_sub(data_contract_id)
        for sub in data_sub:
            sheet.write(row, col, sub['sub_code'])
            sheet.write(row, col + 1, sub['sub_type'])
            sheet.write(row, col + 2, sub['created_date'])
            sheet.write(row, col + 3, sub['price_before_vat'])
            sheet.write(row, col + 4, sub['vat'])
            sheet.write(row, col + 5, sub['price_after_vat'])
            row += 1

        # asset_increase: tang tai san
        row += 1
        col = 0
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_asset_increase()['title_asset_increase'],
                          bold_title_center)
        row += 1
        title_table_asset_increase = self.get_title_table_asset_increase()
        for title in title_table_asset_increase:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_asset_increase = self.get_data_asset_increase(data_contract_id)
        for asset_increase in data_asset_increase:
            sheet.write(row, col, asset_increase['asset_type'])
            sheet.write(row, col + 1, asset_increase['increase_type'])
            sheet.write(row, col + 2, asset_increase['price'])
            sheet.write(row, col + 3, asset_increase['increase_date'])
            sheet.write(row, col + 4, asset_increase['description'])
            row += 1

        # acceptance_payment: nghiem thu thanh toan
        row += 1
        col = 0
        sheet.merge_range('A{}:I{}'.format(row, row + 1), self.get_title_acceptance_payment()['title_acceptance_payment'],
                          bold_title_center)
        row += 1
        title_table_acceptance_payment = self.get_title_table_acceptance_payment()
        for title in title_table_acceptance_payment:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_acceptance_payment = self.get_data_acceptance_payment(data_contract_id)
        for acceptance_payment in data_acceptance_payment:
            sheet.write(row, col, acceptance_payment['acceptance_document_number'])
            sheet.write(row, col + 1, acceptance_payment['acceptance_document_name'])
            sheet.write(row, col + 2, acceptance_payment['acceptance_information'])
            sheet.write(row, col + 3, acceptance_payment['payment_number'])
            sheet.write(row, col + 4, acceptance_payment['payment_employee'])
            sheet.write(row, col + 5, acceptance_payment['payment_information'])
            row += 1
