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


class ReportContractList(models.AbstractModel):
    _name = "report.vnitpro_contract.report_gen_contract_list"

    def get_title_report(self):
        data = {}
        time = datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        time = _('Report Date: ') + time
        title_report = _('Contract List Report')
        data.update({'time_report': time, 'title_report': title_report})
        return data

    def get_title_table(self):
        return [_('Contract Code'), _('Contract Name'), _('Bidder A'), _('Bidder B'), _('Contract Cost'), _('Currency'),
                _('Contract Creator'), _('Contract Create Date'), _('Status'), _('Contract Type')]

    def get_data(self, data):
        contract_ids = self.env['vnitpro.contract'].browse(data['contract_ids'])
        list_contract = []
        for contract in contract_ids:
            if contract.status == 'pending':
                status = (_('Pending'))
            elif contract.status == 'in_process':
                status = (_('In Process'))
            elif contract.status == 'liquidated':
                status = (_('Liquidated'))
            elif contract.status == 'finalized':
                status = (_('Finalized'))
            elif contract.status == 'on_hold':
                status = (_('On Hold'))
            elif contract.status == 'cancel':
                status = (_('Cancel'))
            tz_current = pytz.timezone(self.env.user.partner_id.tz)  # get timezone user
            tz_database = pytz.timezone('UTC')
            create_date = tz_database.localize(datetime.strptime(contract.create_date, '%Y-%m-%d %H:%M:%S'))
            create_date = create_date.astimezone(tz_current)
            create_date = create_date.strftime(_('%m-%d-%Y %H:%M:%S'))
            details = {
                'code': contract.code,
                'name': contract.name,
                'bidder_a': contract.bidder_a.name,
                'bidder_b': contract.bidder_b.name,
                'contract_cost': base.check_number(self, contract.real_cost_after_vat),
                'currency': contract.currency.code,
                'contract_creator': contract.contract_creator.display_name if contract.contract_creator.display_name else '',
                'contract_create_date': create_date,
                'status': status,
                'contract_type_id': contract.contract_type_id.name,
            }
            list_contract.append(details)
        return list_contract

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
