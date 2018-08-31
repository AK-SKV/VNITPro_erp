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


class ReportProcurementList(models.AbstractModel):
    _name = "report.vnitpro_procurement.report_gen_procurement_list"

    def get_title_report(self):
        data = {}
        time = datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        time = _('Report Date: ') + time
        title_report = _('Procurement List Report')
        data.update({'time_report': time, 'title_report': title_report})
        return data

    def get_title_table(self):
        return [_('Procurement Code'), _('Procurement Name'), _('Time Bidder Selection'),
                _('Time Contractors Duration'), _('Funds'), _('Time Invitation'),
                _('Time Bidding'), _('Date Open Profile'), _('Time Review'),
                _('Negotiation Schedule'), _('Bidder Won'),
                _('Value Procurement'), _('Value Won'), _('Currency')]

    def get_data(self, data):
        procurement_ids = self.env['vnitpro.procurement'].browse(data['procurement_ids'])
        list_procurement = []
        for procurement in procurement_ids:
            if procurement.confirm_status == 'draft':
                confirm_status = _('Draft')
            else:
                confirm_status = _('Comfirmed')
            from_date_bidder_select = datetime.strptime(procurement.from_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            to_date_bidder_select = datetime.strptime(procurement.to_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            start_date_contract_duration = datetime.strptime(procurement.start_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            expire_date_contract_duration = datetime.strptime(
                procurement.expire_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            funds = ''
            if len(procurement.funds) == 1:
                funds = '- ' + procurement.funds.name
            else:
                for procurement_funds in procurement.funds:
                    funds += '- ' + procurement_funds.name + '\n'
            time_invitation = ''
            _logger.warning(procurement.approved)
            if procurement.release_time and procurement.bid_submission_deadline:
                if procurement.approved:
                    comfirmed = _('Comfirmed')
                else:
                    comfirmed = _('Draft')
                release_time = datetime.strptime(procurement.release_time, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                bid_submission_deadline = datetime.strptime(
                    procurement.bid_submission_deadline, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                time_invitation = comfirmed + _(' From: ') + release_time + _(' To: ') + bid_submission_deadline
            time_bidding = ''
            if procurement.release_time_bidding and procurement.bid_closing_date:
                if procurement.confirmed_bidding_document:
                    confirmed_bidding_document = _('Comfirmed')
                else:
                    confirmed_bidding_document = _('Draft')
                release_time_bidding = datetime.strptime(
                    procurement.release_time_bidding, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                bid_closing_date = datetime.strptime(procurement.bid_closing_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                time_bidding = confirmed_bidding_document + \
                    _(' - From: ') + release_time_bidding + _(' To: ') + bid_closing_date
            date_open_file = ''
            if procurement.date_open_file:
                date_open_file = datetime.strptime(procurement.date_open_file, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            time_review = ''
            if procurement.review_start and procurement.review_end:
                review_end = datetime.strptime(procurement.review_end, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                review_start = datetime.strptime(procurement.review_start, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                time_review = _(' From: ') + review_start + _(' To: ') + review_end
            new_history = ''
            if procurement.new_history:
                new_history = datetime.strptime(procurement.new_history, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
            bidder_won = ''
            value_procurement = ''
            if procurement.after_tax:
                value_procurement = base.check_number(self, procurement.after_tax)
            value_won = ''
            if len(procurement.expertise_result_ids) > 0:
                for expertise_result_id in procurement.expertise_result_ids:
                    if expertise_result_id.expertise_results == 1:
                        bidder_won = expertise_result_id.negotiation_result_id.ranking_list_id.bid_profile_id.name
                        value_won = base.check_number(self, expertise_result_id.exposure_price_with_vat)
                        break
            details = {
                'name': procurement.name,
                'code': procurement.code,
                'time_bidder_select': confirm_status + _(' From: ') + from_date_bidder_select + _(' To: ') + to_date_bidder_select,
                'time_contract_duration': _('From: ') + start_date_contract_duration + _(' To: ') + expire_date_contract_duration,
                'funds': funds,
                'time_invitation': time_invitation,
                'time_bidding': time_bidding,
                'date_open_file': date_open_file,
                'time_review': time_review,
                'new_history': new_history,
                'bidder_won': bidder_won,
                'currency': procurement.currency_confirm_id.code if procurement.currency_confirm_id else '',
                'value_procurement': value_procurement,
                'value_won': value_won,
            }
            list_procurement.append(details)
        return list_procurement

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        lang = self.env.user.partner_id.lang
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'lang': lang,
            'get_title_report': self.get_title_report,
            'get_data': self.get_data,
            'get_title_table': self.get_title_table,
        }
        return docargs
