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


class ReportContractListDetail(models.AbstractModel):
    _name = "report.vnitpro_contract.report_gen_contract_list_detail"

    def get_title_report(self):
        data = {}
        time_report = datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time_report = tz_database.localize(time_report)
        time_report = time_report.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        time_report = _('Report Date: ') + time_report
        title_report = _('Contract Detail Report')
        data.update({'time_report': time_report, 'title_report': title_report})
        return data

    def get_data_contract(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        data_result = []
        # bidder_a: nhà thầu bên A
        data_result.append([(_('Bidder A')), contract_id.bidder_a.name])
        # bidder_b: nhà thầu bên B
        data_result.append([(_('Bidder B')), contract_id.bidder_b.name])
        # contract_date: ngày ký hợp đồng
        data_result.append(
            [(_('Contract Date')), datetime.strptime(contract_id.contract_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))])
        # contract_formality: hinh thuc hop dong
        data_result.append([(_('Contract Formality')), contract_id.contract_formality_id.name])
        # expire_date - start_date số ngày thực hiện
        for contract in contract_id:
            if contract.unit == 'day':
                unit = (_('day'))
            elif contract.unit == 'week':
                unit = (_('week'))
            elif contract.unit == 'month':
                unit = (_('month'))
            elif contract.unit == 'year':
                unit = (_('year'))
        data_result.append([(_('Contract Duration')), str(contract.duration) + ' ' + unit])
        # cost_before_vat: gia tri truoc thue ban dau
        data_result.append(
            [(_('Cost Before VAT')), base.check_number(self, contract_id.cost_before_vat)])
        # vat_cost: gia tri thue
        data_result.append([(_('VAT Cost')), base.check_number(self, contract_id.vat_cost)])
        # cost_after_vat: gia tri sau thue ban dau
        data_result.append([(_('Cost After VAT')), base.check_number(self, contract_id.cost_after_vat)])
        # currency: tien te
        data_result.append([(_('Currency')), contract_id.currency.code])
        # purpose_of_use: muc dich su dung
        purpose_of_use = ''
        for purpose_of_use_id in contract_id.purpose_of_use:
            if purpose_of_use == '':
                purpose_of_use = purpose_of_use_id.name
            else:
                purpose_of_use += ';' + purpose_of_use_id.name
        data_result.append([(_('Purpose of Use')), purpose_of_use])
        # real_cost_after_vat: gia tri thuc
        data_result.append([(_('Real Cost After VAT')), base.check_number(self, contract_id.real_cost_after_vat)])
        # code: ma hop dong
        data_result.append([(_('Contract Code')), contract_id.code])
        # contract_type: ma hop dong
        data_result.append([(_('Contract Type')), contract_id.contract_type_id.name])
        # name: ten hop dong
        data_result.append([(_('Contract Name')), contract_id.name])
        # name: ten nguoi tao
        display_name = ''
        employee = self.env['vnitpro.employee'].search([('res_user_id', '=', contract_id.create_uid.id)], limit=1)
        if employee:
            display_name = employee.display_name
        data_result.append([(_('Contract Creator')), display_name])
        # start_date: ngay bat dau thuc hien hop dong
        data_result.append([(_('Contract Start Date')), datetime.strptime(contract_id.start_date, '%Y-%m-%d').strftime(
            _('%m-%d-%Y'))])
        # package_price: Giá trị hạng mục trọn gói
        data_result.append([(_('Package Price')), base.check_number(self, contract_id.package_price)])
        # adjusted_price: Giá trị hạng mục đơn giá điều chỉnh
        data_result.append([(_('Adjusted Price')), base.check_number(self, contract_id.adjusted_price)])
        # permanent_price: Giá trị hạng mục đơn giá cố định
        data_result.append([(_('Permanent Price')), base.check_number(self, contract_id.permanent_price)])
        # vat: thuế VAT
        for contract in contract_id:
            vat = ''
            if contract.vat == '0':
                vat = '0%'
            elif contract.vat == '5':
                vat = '5%'
            elif contract.vat == '10':
                vat = '10%'
        data_result.append([(_('VAT %')), vat])
        # funds: nguồn vốn
        data_result.append([(_('Funds')), contract_id.funds.name])
        # real_cost_before_vat: giá trị trước thuế
        data_result.append([(_('Real Cost Before VAT')), base.check_number(self, contract_id.real_cost_before_vat)])
        # description: mô tả
        data_result.append([(_('Description')), contract_id.description if contract_id.description else ''])
        # guarantee_unit: đơn vị bảo lãnh
        guarantee_unit = ''
        if contract_id.guarantee_unit:
            guarantee_unit = contract_id.guarantee_unit
        data_result.append([(_('Guarantee Unit')), guarantee_unit])
        # guarantee_start_date: ngày bắt đầu bảo lãnh
        guarantee_start_date = ''
        if contract_id.guarantee_start_date:
            guarantee_start_date = datetime.strptime(contract_id.guarantee_start_date, '%Y-%m-%d').strftime(
                _('%m-%d-%Y'))
        data_result.append([(_('Guarantee Start Date')), guarantee_start_date])
        # guarantee_end_date: ngày kết thúc bảo lãnh
        guarantee_end_date = ''
        if contract_id.guarantee_end_date:
            guarantee_end_date = datetime.strptime(contract_id.guarantee_end_date, '%Y-%m-%d').strftime(
                _('%m-%d-%Y'))
        data_result.append([(_('Guarantee End Date')), guarantee_end_date])
        # guarantee_price: giá trị bảo lãnh
        data_result.append([(_('Guarantee Price')), base.check_number(self,
                                                                      contract_id.guarantee_price) if contract_id.guarantee_price else ''])
        # note : ghi chú
        data_result.append([(_('Note')), contract_id.note if contract_id.note else ''])
        return data_result

    # guarantee: bao lanh

    def get_title_guarantee(self):
        return {'title_guarantee': _('Guarantee Contract List')}

    def get_title_table_guarantee(self):
        return [_('Guarantee Type'), _('Guarantee Unit'),
                _('Status'), _('Create Date'), _('Start Date'),
                _('End Date'), _('Price'), _('Note')]

    def get_data_guarantee(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_guarantee = []
        if contract_id.guarantee_ids:
            for guarantee in contract_id.guarantee_ids:
                note = ''
                if guarantee.note:
                    note = guarantee.note
                status = ''
                if guarantee.status == 1:
                    status = _('Effect')
                elif guarantee.status == 2:
                    status = _('Expired')
                tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
                tz_database = pytz.timezone('UTC')
                create_date = tz_database.localize(datetime.strptime(guarantee.create_date, '%Y-%m-%d %H:%M:%S'))
                create_date = create_date.astimezone(tz_current)
                create_date = create_date.strftime(_('%m-%d-%Y %H:%M:%S'))
                detail = {
                    'guarantee_type': guarantee.guarantee_type.name,
                    'guarantee_unit': guarantee.guarantee_unit,
                    'status': status,
                    'create_date': create_date,
                    'start_date': datetime.strptime(guarantee.start_date, '%Y-%m-%d').strftime(_('%m-%d-%Y')),
                    'end_date': datetime.strptime(guarantee.end_date, '%Y-%m-%d').strftime(_('%m-%d-%Y')),
                    'price': base.check_number(self, guarantee.price),
                    'note': note,
                }
                list_guarantee.append(detail)
        return list_guarantee

    # category: hạng mục hợp đồng

    def get_title_category(self):
        return {'title_category': _('Category Contract List')}

    def get_title_table_category(self):
        return [_('Code Number'), _('Category Name'), _('Quantity'), _('Unit Price'), _('VAT %'), _('Price After VAT'),
                _('Warranty Period(months)'), _('Employee import')]

    def get_data_category(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_category = []
        if contract_id.contract_category_ids:
            for category in contract_id.contract_category_ids:
                vat = ''
                if category.vat == 0:
                    vat = '0%'
                elif category.vat == 5:
                    vat = '5%'
                elif category.vat == 10:
                    vat = '10%'
                str_employee = ''
                employee = self.env['vnitpro.employee'].search([('res_user_id', '=', category.create_uid.id)], limit=1)
                if employee:
                    str_employee = employee.display_name
                detail = {
                    'code_number': category.code_number,
                    'category': category.category,
                    'quantity': base.check_number(self, category.quantity) + ' {}'.format(category.unit),
                    'unit_price': base.check_number(self, category.unit_price) + ' {}'.format(
                        category.currency_id.code),
                    'vat': vat,
                    'cost_after_vat': base.check_number(self, category.cost_after_vat) + ' {}'.format(
                        category.currency_id.code),
                    'warranty_period': category.warranty_period,
                    'employee': str_employee
                }
                list_category.append(detail)
        return list_category

    # payment term: dieu khoan thanh toan

    def get_title_payment_term(self):
        return {'title_payment_term': _('Payment Term Contract List')}

    def get_title_table_payment_term(self):
        return [_('Payment Name'), _('Start Date'),
                _('End Date'), _('Payment Price'), _('Description')]

    def get_data_payment_term(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_payment_term = []
        if contract_id.payment_term_ids:
            for payment_term in contract_id.payment_term_ids:
                description = ''
                if payment_term.description:
                    description = payment_term.description
                detail = {
                    'payment_name': payment_term.payment_name,
                    'start_date': datetime.strptime(payment_term.start_date, '%Y-%m-%d').strftime(_('%m-%d-%Y')),
                    'end_date': datetime.strptime(payment_term.end_date, '%Y-%m-%d').strftime(_('%m-%d-%Y')),
                    'payment_price': base.check_number(self, payment_term.payment_price),
                    'description': description,
                }
                list_payment_term.append(detail)
        return list_payment_term

    # sub: phu luc

    def get_title_sub(self):
        return {'title_sub': _('Sub Contract List')}

    def get_title_table_sub(self):
        return [_('Sub Code'), _('Sub Type'),
                _('Create Date'), _('Price Before VAT'),
                _('VAT %'), _('Price Sub')]

    def get_data_sub(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_sub = []
        if contract_id.contract_sub_ids:
            for sub in contract_id.contract_sub_ids:
                create_date = ''
                if sub.created_date:
                    create_date = datetime.strptime(sub.created_date, '%Y-%m-%d').strftime(_('%m-%d-%Y'))
                price_before_vat = ''
                price_after_vat = ''
                if sub.price_before_vat:
                    price_before_vat = base.check_number(self, sub.price_before_vat)
                    price_after_vat = base.check_number(self, sub.price_after_vat)
                vat = ''
                if sub.vat == 0:
                    vat = '0%'
                elif sub.vat == 5:
                    vat = '5%'
                elif sub.vat == 10:
                    vat = '10%'
                detail = {
                    'sub_code': sub.sub_code,
                    'sub_type': sub.sub_type.name,
                    'created_date': create_date,
                    'price_before_vat': price_before_vat,
                    'vat': vat,
                    'price_after_vat': price_after_vat,
                }
                list_sub.append(detail)
        return list_sub

    # asset_increase: tang tai san

    def get_title_asset_increase(self):
        return {'title_asset_increase': _('Asset Increase List')}

    def get_title_table_asset_increase(self):
        return [_('Asset Type'), _('Increase Type'),
                _('Price'), _('Increase Date'), _('Description')]

    def get_data_asset_increase(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_asset_increase = []
        if contract_id.asset_increase_ids:
            for asset_increase in contract_id.asset_increase_ids:
                increase_type = ''
                if asset_increase.increase_type == 1:
                    increase_type = _('Official')
                elif asset_increase.increase_type == 2:
                    increase_type = _('Temporary')
                description = ''
                if asset_increase.description:
                    description = asset_increase.description
                detail = {
                    'asset_type': asset_increase.asset_type.name,
                    'increase_type': increase_type,
                    'price': base.check_number(self, asset_increase.price),
                    'increase_date': datetime.strptime(asset_increase.increase_date, '%Y-%m-%d').strftime(
                        _('%m-%d-%Y')),
                    'description': description,
                }
                list_asset_increase.append(detail)
        return list_asset_increase

    # acceptance_payment: nghiem thu thanh toan

    def get_title_acceptance_payment(self):
        return {'title_acceptance_payment': _('Acceptance - Payment List')}

    def get_title_table_acceptance_payment(self):
        return [_('Acceptance Document Number'), _('Acceptance Document Name'),
                _('Acceptance Information'), _('Payment Number'), _('Payment Employee'), _('Payment Detail')]

    def get_data_acceptance_payment(self, data):
        contract_id = self.env['vnitpro.contract'].browse(data['contract_id'])
        list_acceptance_payment = []
        if contract_id.acceptance_payment_ids:
            for acceptance_payment in contract_id.acceptance_payment_ids:
                acceptance_information = ''
                if acceptance_payment.acceptance_information:
                    acceptance_information = acceptance_payment.acceptance_information
                payment_information = ''
                if acceptance_payment.payment_information:
                    payment_information = acceptance_payment.payment_information
                detail = {
                    'acceptance_document_number': acceptance_payment.acceptance_document_number,
                    'acceptance_document_name': acceptance_payment.acceptance_document_name,
                    'acceptance_information': acceptance_information,
                    'payment_number': acceptance_payment.payment_number,
                    'payment_employee': acceptance_payment.payment_employee.name,
                    'payment_information': payment_information,
                }
                list_acceptance_payment.append(detail)
        return list_acceptance_payment

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
            'get_data_contract': self.get_data_contract,
            'get_title_guarantee': self.get_title_guarantee,
            'get_title_table_guarantee': self.get_title_table_guarantee,
            'get_data_guarantee': self.get_data_guarantee,
            'get_title_category': self.get_title_category,
            'get_title_table_category': self.get_title_table_category,
            'get_data_category': self.get_data_category,
            'get_title_payment_term': self.get_title_payment_term,
            'get_title_table_payment_term': self.get_title_table_payment_term,
            'get_data_payment_term': self.get_data_payment_term,
            'get_title_sub': self.get_title_sub,
            'get_title_table_sub': self.get_title_table_sub,
            'get_data_sub': self.get_data_sub,
            'get_title_asset_increase': self.get_title_asset_increase,
            'get_title_table_asset_increase': self.get_title_table_asset_increase,
            'get_data_asset_increase': self.get_data_asset_increase,
            'get_title_acceptance_payment': self.get_title_acceptance_payment,
            'get_title_table_acceptance_payment': self.get_title_table_acceptance_payment,
            'get_data_acceptance_payment': self.get_data_acceptance_payment,
        }
        return docargs
