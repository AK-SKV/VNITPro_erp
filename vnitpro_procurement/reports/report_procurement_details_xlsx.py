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
    _name = 'report.vnitpro_procurement.report_gen_procurement_details_xlsx'
    _inherit = 'report.vnitpro_procurement.report_gen_procurement_details', 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet(_('Procurement Detail'))
        bold = workbook.add_format({'bold': True, 'border': 1, 'font_size': 14})
        left = workbook.add_format({'align': 'left', 'border': 1, 'font_size': 13})
        center = workbook.add_format({'align': 'center', 'border': 1, 'font_size': 13})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14, 'border': 1})
        bold_title_center = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 16})
        italic = workbook.add_format({'italic': True})
        title_line_format = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'})
        date_line_format = workbook.add_format(
            {'italic': True, 'font_size': 15, 'align': 'center', 'bold': True, 'valign': 'vcenter'})
        date_format = workbook.add_format({'num_format': _('mm-dd-yyyy')})
        sheet.set_column('A:M', 18)
        row = 0
        col = 0

        # Tiêu đề báo cáo
        data_title = self.get_title_report()
        row += 5
        sheet.merge_range('A1:K3', data_title['title_report'], title_line_format)
        sheet.merge_range('A4:K5', data_title['time_report'], date_line_format)

        # Dữ liệu bảng báo cáo
        row += 1
        data_procurement_id = {}
        data_procurement_id.update({'procurement_ids': partners.id})
        # Thông tin gói thầu & Duyệt kế hoạch đấu thầu
        row += 1
        sheet.merge_range('A{}:E{}'.format(row, row + 1), _('Procurement Information'), bold_title_center)
        sheet.merge_range('G{}:K{}'.format(row, row + 1), _('Confirm Procurement'), bold_title_center)

        row += 2
        row1 = row
        row2 = row
        data_procurement = self.get_data_information(data_procurement_id)
        for procurement in data_procurement:
            sheet.merge_range('A{}:B{}'.format(row1, row1), procurement[0], bold)
            sheet.merge_range('C{}:E{}'.format(row1, row1), procurement[1], left)
            row1 += 1
        data_procurement = self.get_data_confirm(data_procurement_id)
        for procurement in data_procurement:
            sheet.merge_range('G{}:H{}'.format(row2, row2), procurement[0], bold)
            sheet.merge_range('I{}:K{}'.format(row2, row2), procurement[1], left)
            row2 += 1
        row = row1

        # Hợp đồng tư vấn đấu thầu & Hồ sơ mời thầu sơ tuyển
        row += 1
        sheet.merge_range('A{}:E{}'.format(row, row + 1), _('Advisory Procurement'), bold_title_center)
        sheet.merge_range('G{}:K{}'.format(row, row + 1), _('Invitation PQ Documents'), bold_title_center)
        row += 2
        row1 = row
        row2 = row
        data_procurement = self.get_data_advisory(data_procurement_id)
        for procurement in data_procurement:
            sheet.merge_range('A{}:B{}'.format(row1, row1), procurement[0], bold)
            sheet.merge_range('C{}:E{}'.format(row1, row1), procurement[1], left)
            row1 += 1
        data_procurement = self.get_data_invitation(data_procurement_id)
        for procurement in data_procurement:
            sheet.merge_range('G{}:H{}'.format(row2, row2), procurement[0], bold)
            sheet.merge_range('I{}:K{}'.format(row2, row2), procurement[1], left)
            row2 += 1
        row = row1

        # Ghi nhận hồ sơ sơ tuyển
        row += 1
        sheet.merge_range('A{}:F{}'.format(row, row + 1), _('Approve PQ Documents'), bold_title_center)
        row += 1
        title_approve = self.get_title_approve()
        for title in title_approve:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_approve = self.get_data_approve(data_procurement_id)
        for approve in data_approve:
            sheet.write(row, col, approve['code'], center)
            sheet.write(row, col + 1, approve['name'], center)
            sheet.write(row, col + 2, approve['bidder'], center)
            sheet.write(row, col + 3, approve['document_submission_date'], center)
            sheet.write(row, col + 4, approve['submission_name'], center)
            sheet.write(row, col + 5, approve['contact_information'], center)
            row += 1

        # Danh sách duyệt sơ tuyển
        row += 1
        sheet.merge_range('A{}:G{}'.format(row, row + 1), _('Confirm Prequalification'), bold_title_center)
        row += 1
        title_confirm_prequalification = self.get_title_confirm_prequalification()
        for title in title_confirm_prequalification:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_confirm_prequalification = self.get_data_confirm_prequalification(data_procurement_id)
        for confirm_prequalification in data_confirm_prequalification:
            sheet.write(row, col, confirm_prequalification['approve_pq_document_id'], center)
            sheet.write(row, col + 1, confirm_prequalification['expertise_team_leader'], center)
            sheet.write(row, col + 2, confirm_prequalification['expertise_team_member'], center)
            sheet.write(row, col + 3, confirm_prequalification['expert_team_leader'], center)
            sheet.write(row, col + 4, confirm_prequalification['expert_team_member'], center)
            sheet.write(row, col + 5, confirm_prequalification['bid_submission_deadline'], center)
            sheet.write(row, col + 6, confirm_prequalification['result'], center)
            row += 1

        # Hồ sơ mời thầu
        row += 1
        sheet.merge_range('A{}:E{}'.format(row, row + 1), _('Bidding Document'), bold_title_center)
        row += 2
        data_procurement = self.get_data_bidding_document(data_procurement_id)
        for procurement in data_procurement:
            sheet.merge_range('A{}:B{}'.format(row, row), procurement[0], bold)
            sheet.merge_range('C{}:E{}'.format(row, row), procurement[1], left)
            row += 1

        # Hồ sơ dự thầu/ Hồ sơ đề xuất
        row += 1
        sheet.merge_range('A{}:F{}'.format(row, row + 1), _('Bid Profile/ Offer Profile'), bold_title_center)
        row += 1
        title_bid_profile = self.get_title_bid_profile()
        for title in title_bid_profile:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_bid_profile = self.get_data_bid_profile(data_procurement_id)
        for bid_profile in data_bid_profile:
            sheet.write(row, col, bid_profile['code'], center)
            sheet.write(row, col + 1, bid_profile['name'], center)
            sheet.write(row, col + 2, bid_profile['bidder'], center)
            sheet.write(row, col + 3, bid_profile['document_submission_date'], center)
            sheet.write(row, col + 4, bid_profile['submission_name'], center)
            sheet.write(row, col + 5, bid_profile['contact_information'], center)
            row += 1

        # Danh sách xếp hạng
        row += 1
        sheet.merge_range('A{}:J{}'.format(row, row + 1), _('Ranking List'), bold_title_center)
        row += 1
        title_ranking_list = self.get_title_ranking_list()
        for title in title_ranking_list:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_ranking_list = self.get_data_ranking_list(data_procurement_id)
        for ranking_list in data_ranking_list:
            sheet.write(row, col, ranking_list['bid_profile_id'], center)
            sheet.write(row, col + 1, ranking_list['point'], center)
            sheet.write(row, col + 2, ranking_list['date_of_bid'], center)
            sheet.write(row, col + 3, ranking_list['the_price_includes_vat'], center)
            sheet.write(row, col + 4, ranking_list['discount'], center)
            sheet.write(row, col + 5, ranking_list['expertise_team_leader'], center)
            sheet.write(row, col + 6, ranking_list['expertise_team_member'], center)
            sheet.write(row, col + 7, ranking_list['expert_team_leader'], center)
            sheet.write(row, col + 8, ranking_list['expert_team_member'], center)
            sheet.write(row, col + 9, ranking_list['result'], center)
            row += 1

        # Kết quả thương thảo
        row += 1
        sheet.merge_range('A{}:H{}'.format(row, row + 1), _('Negotiation Results'), bold_title_center)
        row += 1
        title_negotiation_results = self.get_title_negotiation_results()
        for title in title_negotiation_results:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_negotiation_results = self.get_data_negotiation_results(data_procurement_id)
        for negotiation_results in data_negotiation_results:
            sheet.write(row, col, negotiation_results['ranking_list_id'], center)
            sheet.write(row, col + 1, negotiation_results['negotiation_result'], center)
            sheet.write(row, col + 2, negotiation_results['after_tax'], center)
            sheet.write(row, col + 3, negotiation_results['the_negotiated_price_includes_vat'], center)
            sheet.write(row, col + 4, negotiation_results['price_difference'], center)
            sheet.write(row, col + 5, negotiation_results['date_negotiation'], center)
            sheet.write(row, col + 6, negotiation_results['negotiation_team_leader'], center)
            sheet.write(row, col + 7, negotiation_results['negotiation_team_member'], center)
            row += 1

        # Thẩm định lựa chọn nhà thầu
        row += 1
        sheet.merge_range('A{}:I{}'.format(row, row + 1), _('Negotiation Results'), bold_title_center)
        row += 1
        title_expertise = self.get_title_expertise()
        for title in title_expertise:
            sheet.write(row, col, title, bold_center)
            col += 1
        row += 1
        col = 0
        data_expertise = self.get_data_expertise(data_procurement_id)
        for expertise in data_expertise:
            sheet.write(row, col, expertise['negotiation_result_id'], center)
            sheet.write(row, col + 1, expertise['expertise_start_date'], center)
            sheet.write(row, col + 2, expertise['expertise_end_date'], center)
            sheet.write(row, col + 3, expertise['expertise_results'], center)
            sheet.write(row, col + 4, expertise['exposure_price_with_vat'], center)
            sheet.write(row, col + 5, expertise['number_of_the_selected_bid'], center)
            sheet.write(row, col + 6, expertise['decided_date'], center)
            sheet.write(row, col + 7, expertise['expertise_team_leader'], center)
            sheet.write(row, col + 7, expertise['expertise_team_member'], center)
            row += 1
