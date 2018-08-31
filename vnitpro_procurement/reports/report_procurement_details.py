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

_logger = logging.getLogger(__name__)


class ReportProcurementList(models.AbstractModel):
    _name = "report.vnitpro_procurement.report_gen_procurement_details"

    def change_format_date(self, date):
        try:
            date_format = datetime.strptime(date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            return date_format
        except:
            return ''

    def get_title_report(self):
        data = {}
        time = datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        time = _('Report Date: ') + time
        title_report = _('Procurement Details Report')
        data.update({'time_report': time, 'title_report': title_report})
        return data
    # Thông tin gói thầu

    def get_data_information(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids:
            arena = ''
            if procurement.arena:
                if procurement.arena == 'inland':
                    arena = _('Inland')
                else:
                    arena = _('International')
            procurement_type = ''
            if procurement.procurement_type:
                if procurement.procurement_type == '1':
                    procurement_type = _('Provide Non-Consulting Services')
                elif procurement.procurement_type == '2':
                    procurement_type = _('Composite')
                elif procurement.procurement_type == '3':
                    procurement_type = _('Merchandise Shoping')
                elif procurement.procurement_type == '4':
                    procurement_type = _('Selective﻿ Advisory')
                else:
                    procurement_type = _('Build')
            procurement_method = ''
            if procurement.procurement_method:
                if procurement.procurement_method == '1':
                    procurement_method = _('Two Packpage')
                elif procurement.procurement_method == '2':
                    procurement_method = _('One Packpage')
                else:
                    procurement_method = _('Following The Shortened Procedure')
            type_of_contract = ''
            if procurement.type_of_contract:
                if procurement.type_of_contract == '1':
                    type_of_contract = _('By Fixed Price')
                elif procurement.type_of_contract == '2':
                    type_of_contract = _('By Adjusted Value')
                elif procurement.type_of_contract == '3':
                    type_of_contract = _('By Time')
                else:
                    type_of_contract = _('By Package')
            funds = ''
            if procurement.funds:
                for i in range(0, len(procurement.funds)):
                    if i == len(procurement.funds) - 1:
                        funds += procurement.funds[i].name
                    else:
                        funds += procurement.funds[i].name + ' - '
            contractors_selection = ''
            if procurement.from_date and procurement.to_date:
                contractors_selection = _('From: ') + self.change_format_date(procurement.from_date) + \
                    _(' To: ') + self.change_format_date(procurement.to_date)
            data_result.append([_('Procurement Code'), procurement.code])
            data_result.append([_('Procurement Name'), procurement.name])
            data_result.append([_('Arena'), arena])
            data_result.append([_('Procurement type'), procurement_type])
            data_result.append([_('Procurement Selection Form'), procurement.procurement_formality_id.name])
            data_result.append([_('Procurement Method'), procurement_method])
            data_result.append([_('Contractors Selection'), contractors_selection])
            data_result.append([_('Type Of Contract'), type_of_contract])
            data_result.append([_('Funds'), funds])

        return data_result
    # Duyệt kế hoạch đấu thầu

    def get_data_confirm(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids:
            vat_confirm = ''
            if procurement.vat_confirm:
                if procurement.vat_confirm == 0:
                    vat_confirm = _('0 %')
                elif procurement.vat_confirm == 5:
                    vat_confirm = _('5 %')
                else:
                    vat_confirm = _('10 %')
            else:
                vat_confirm = ''

            data_result.append([_('Number Of Approval Decision'),
                                procurement.code_confirm if procurement.code_confirm else ''])
            data_result.append([_('Approval Date'), self.change_format_date(
                procurement.approval_date) if procurement.approval_date else ''])
            data_result.append(
                [_('Approver'), procurement.approver.display_name if procurement.approver.display_name else ''])
            data_result.append([_('Before Tax'), procurement.before_tax if procurement.before_tax else ''])
            data_result.append([_('% VAT'), vat_confirm])
            data_result.append([_('Money Tax'), procurement.money_tax if procurement.money_tax else ''])
            data_result.append([_('After Tax'), procurement.after_tax if procurement.after_tax else ''])
            data_result.append(
                [_('Currency'), procurement.currency_confirm_id.code if procurement.currency_confirm_id.code else ''])

        return data_result
    # Hợp đồng tư vấn đấu thầu

    def get_data_advisory(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids:
            type_of_contract_advisory = ''
            if procurement.type_of_contract_advisory:
                if procurement.type_of_contract_advisory == '1':
                    type_of_contract_advisory = _('By Fixed Price')
                elif procurement.type_of_contract_advisory == '2':
                    type_of_contract_advisory = _('By Adjusted Value')
                elif procurement.type_of_contract_advisory == '3':
                    type_of_contract_advisory = _('By Time')
                elif procurement.type_of_contract_advisory == '4':
                    type_of_contract_advisory = _('By Package')
            created_advision = ''
            if procurement.created_advision == True:
                created_advision = _('Approved')
            else:
                created_advision = _('Unapproved')
            funds_advisory = ''
            if procurement.funds_advisory:
                for i in range(0, len(procurement.funds_advisory)):
                    if i == len(procurement.funds_advisory) - 1:
                        funds_advisory += procurement.funds_advisory[i].name
                    else:
                        funds_advisory += procurement.funds_advisory[i].name + ' - '
            duration = ''
            if procurement.from_date_ad and procurement.to_date_ad:
                duration = _('From: ') + self.change_format_date(procurement.from_date_ad) + \
                    _(' To: ') + self.change_format_date(procurement.to_date_ad)

            data_result.append([_('Code Advisory'), procurement.code_advisory if procurement.code_advisory else ''])
            data_result.append([_('Name Advisory'), procurement.name_advisory if procurement.name_advisory else ''])
            data_result.append([_('Bidder A'), procurement.bidder_a.name if procurement.bidder_a else ''])
            data_result.append([_('Bidder B'), procurement.bidder_b.name if procurement.bidder_b else ''])
            data_result.append([_('Type Of Contract'), type_of_contract_advisory])
            data_result.append([_('Contract After VAT'), procurement.contract_after_vat])
            data_result.append(
                [_('Currency'), procurement.currency_confirm_id.code if procurement.currency_confirm_id.code else ''])
            data_result.append([_('Duration Of Contract'), duration])
            data_result.append([_('Funds'), funds_advisory])
            data_result.append([_('Created Advisory Procurement'), created_advision])

        return data_result
    # Hồ sơ mời thầu sơ tuyển

    def get_data_invitation(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids:
            approved = ''
            if procurement.approved == True:
                approved = _('Approved')
            else:
                approved = _('Unapproved')

            data_result.append([_('Profile Code'), procurement.code_profile if procurement.code_profile else ''])
            data_result.append([_('Profile Name'), procurement.name_profile if procurement.code_profile else ''])
            data_result.append([_('Release Time'), self.change_format_date(
                procurement.release_time) if procurement.release_time else ''])
            data_result.append([_('Bid Submission Deadline'),
                                self.change_format_date(procurement.bid_submission_deadline) if procurement.bid_submission_deadline else ''])
            data_result.append([_('Approved By The Director'), approved])
            data_result.append([_('Creator'), procurement.creator.name if procurement.creator else ''])

        return data_result
    # Ghi nhận hồ sơ sơ tuyển

    def get_title_approve(self):
        return [_('Profile Code'), _('Profile Name'), _('Bidder'),
                _('Document Submission Date'), _('Submission Name'), _('Contact Information')]

    def get_data_approve(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        if procurement_ids.approve_pq_document_ids:
            for procurement in procurement_ids.approve_pq_document_ids:
                details = {
                    'code': procurement.code,
                    'name': procurement.name,
                    'bidder': procurement.bidder_id.name,
                    'document_submission_date': self.change_format_date(procurement.document_submission_date),
                    'submission_name': procurement.submission_name,
                    'contact_information': procurement.contact_information,
                }
                data_result.append(details)
        return data_result
    # Danh sách duyệt sơ tuyển

    def get_title_confirm_prequalification(self):
        return [_('PQ Document'), _('Expertise Team Leader'), _('Expertise Team Member'),
                _('Expert Team Leader'), _('Expert Team Member'), _('Evaluation Date'), _('Result')]

    def get_data_confirm_prequalification(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids.confirm_pre_ids:
            result = ''
            if procurement.result:
                if procurement.result == 1:
                    result = _('Passed')
                else:
                    result = _('Not Passed')
            details = {
                'approve_pq_document_id': procurement.approve_pq_document_id.name,
                'expertise_team_leader': procurement.expertise_team_leader.name,
                'expertise_team_member': procurement.expertise_team_member.name,
                'expert_team_leader': procurement.expert_team_leader.name,
                'expert_team_member': procurement.expert_team_member.name,
                'bid_submission_deadline': procurement.bid_submission_deadline,
                'result': result,
            }
            data_result.append(details)
        return data_result
    # Hồ sơ mời thầu

    def get_data_bidding_document(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids:
            confirmed_bidding_document = ''
            if procurement.confirmed_bidding_document:
                if procurement.confirmed_bidding_document == True:
                    confirmed_bidding_document = _('Approved')
                else:
                    confirmed_bidding_document = _('Unapproved')
            data_result.append([_('Bidding Document Code'),
                                procurement.bidding_document_code if procurement.bidding_document_code else ''])
            data_result.append([_('Bidding Document Name'),
                                procurement.bidding_document_name if procurement.bidding_document_name else ''])
            data_result.append(
                [_('Release Time'), self.change_format_date(procurement.release_time_bidding) if procurement.release_time_bidding else ''])
            data_result.append(
                [_('Bid Closing Date'), self.change_format_date(procurement.bid_closing_date) if procurement.bid_closing_date else ''])
            data_result.append([_('Date Open File'), self.change_format_date(
                procurement.date_open_file) if procurement.date_open_file else ''])
            data_result.append([_('Review Start Date'), self.change_format_date(
                procurement.review_start) if procurement.review_start else ''])
            data_result.append([_('Review End Date'), self.change_format_date(
                procurement.review_end) if procurement.review_end else ''])
            data_result.append([_('New History'), self.change_format_date(
                procurement.new_history) if procurement.new_history else ''])
            data_result.append([_('Confirmed Bidding Document'), confirmed_bidding_document])
        return data_result
    # Hồ sơ dự thầu/ Hồ sơ đề xuất

    def get_title_bid_profile(self):
        return [_('Profile Code'), _('Profile Name'), _('Bidder'),
                _('Document Submission Date'), _('Submission Name'), _('Contact Information')]

    def get_data_bid_profile(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids.bid_profile_ids:
            details = {
                'code': procurement.code,
                'name': procurement.name,
                'bidder': procurement.bidder_id.name,
                'document_submission_date': self.change_format_date(procurement.document_submission_date),
                'submission_name': procurement.submission_name,
                'contact_information': procurement.contact_information,
            }
            data_result.append(details)
        return data_result
    # Danh sách xếp hạng

    def get_title_ranking_list(self):
        return [_('Bid Profile'), _('Point'), _('Date Of Bid'),
                _('The Price Includes VAT'), _('Discount'), _('Expertise Team Leader'),
                _('Expertise Team Member'), _('Expert Team Leader'), _('Expert Team Member'),
                _('Result')]

    def get_data_ranking_list(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids.ranking_list_ids:
            result = ''
            if procurement.result:
                if procurement.result == 1:
                    result = _('Passed')
                else:
                    result = _('Not Passed')
            expertise_team_member = ''
            if procurement.expertise_team_member:
                expertise_team_member = procurement.expertise_team_member.display_name
            expert_team_member = ''
            if procurement.expert_team_member:
                expert_team_member = procurement.expert_team_member.display_name

            details = {
                'bid_profile_id': procurement.bid_profile_id.name,
                'point': procurement.point,
                'date_of_bid': self.change_format_date(procurement.date_of_bid),
                'the_price_includes_vat': procurement.the_price_includes_vat,
                'discount': procurement.discount,
                'expertise_team_leader': procurement.expertise_team_leader.display_name,
                'expertise_team_member': expertise_team_member,
                'expert_team_leader': procurement.expert_team_leader.display_name,
                'expert_team_member': expert_team_member,
                'result': result,
            }
            data_result.append(details)
        return data_result
    # Kết quả thương thảo

    def get_title_negotiation_results(self):
        return [_('Bid Profile'), _('Negotiation Result'), _('After Tax'),
                _('The Negotiated Price Includes VAT'), _('Price Difference'), _('Date Negotiation'),
                _('Negotiation Team Leader'), _('Negotiation Team Member')]

    def get_data_negotiation_results(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids.negotiation_list_ids:
            negotiation_team_member = ''
            if procurement.negotiation_team_member:
                negotiation_team_member = procurement.negotiation_team_member.display_name
            details = {
                'ranking_list_id': procurement.ranking_list_id.bid_profile_id.name,
                'negotiation_result': procurement.negotiation_result,
                'after_tax': procurement.after_tax,
                'the_negotiated_price_includes_vat': procurement.the_negotiated_price_includes_vat,
                'price_difference': procurement.price_difference,
                'date_negotiation': self.change_format_date(procurement.date_negotiation),
                'negotiation_team_leader': procurement.negotiation_team_leader.display_name,
                'negotiation_team_member': negotiation_team_member,
            }
            data_result.append(details)
        return data_result
    # Thẩm định lựa chọn nhà thầu

    def get_title_expertise(self):
        return [_('Bid Profile Won'), _('Expertise Start Date'), _('Expertise End Date'),
                _('Expertise Results'), _('Exposure Price With VAT'), _('Number Of The Selected Bid'),
                _('Decided Date'), _('Expertise Team Leader'), _('Expertise Team Member')]

    def get_data_expertise(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        data_result = []
        for procurement in procurement_ids.expertise_result_ids:
            expertise_results = ''
            if procurement.expertise_results:
                if procurement.expertise_results == 1:
                    expertise_results = _('Passed')
                else:
                    expertise_results = _('Not Passed')
            expertise_team_member = ''
            if procurement.expertise_team_member:
                expertise_team_member = procurement.expertise_team_member.display_name
            details = {
                'negotiation_result_id': procurement.negotiation_result_id.ranking_list_id.bid_profile_id.name,
                'expertise_start_date': self.change_format_date(procurement.expertise_start_date),
                'expertise_end_date': self.change_format_date(procurement.expertise_end_date),
                'expertise_results': expertise_results,
                'exposure_price_with_vat': procurement.exposure_price_with_vat,
                'number_of_the_selected_bid': procurement.number_of_the_selected_bid,
                'decided_date': self.change_format_date(procurement.decided_date),
                'expertise_team_leader': procurement.expertise_team_leader.display_name,
                'expertise_team_member': expertise_team_member,
            }
            data_result.append(details)
        return data_result

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
            'get_title_report': self.get_title_report,
            'get_data_information': self.get_data_information,
            'get_data_confirm': self.get_data_confirm,
            'get_data_advisory': self.get_data_advisory,
            'get_data_invitation': self.get_data_invitation,
            'get_data_approve': self.get_data_approve,
            'get_title_approve': self.get_title_approve,
            'get_title_confirm_prequalification': self.get_title_confirm_prequalification,
            'get_data_confirm_prequalification': self.get_data_confirm_prequalification,
            'get_data_bidding_document': self.get_data_bidding_document,
            'get_title_bid_profile': self.get_title_bid_profile,
            'get_data_bid_profile': self.get_data_bid_profile,
            'get_title_ranking_list': self.get_title_ranking_list,
            'get_data_ranking_list': self.get_data_ranking_list,
            'get_title_negotiation_results': self.get_title_negotiation_results,
            'get_data_negotiation_results': self.get_data_negotiation_results,
            'get_title_expertise': self.get_title_expertise,
            'get_data_expertise': self.get_data_expertise,
        }
        return docargs
