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


class ReportConsumeProduct(models.AbstractModel):
    _name = "report.vnitpro_consume.report_gen_consume_product"

    def get_title_report(self):
        data = {}
        title_report = _('CONSUME PRODUCT REPORT')
        data.update({'title_report': title_report})
        return data

    def get_data(self, data):
        export_card_list_ids = self.env['vnitpro.inventory.export.product.detail'].browse(data['export_card_ids'])
        direct_export_card_list_ids = self.env['vnitpro.direct.import.product.detail'].browse(
            data['direct_export_card_list_ids'])
        group_product_ids = self.env['vnitpro.product.group'].search([])
        warehouse_ids = self.env['vnitpro.warehouse'].search([])
        list = []
        group_product_sequence = 0
        for group_product_id in group_product_ids:
            group_product_sequence += 1
            list_id = {
                'sequence': group_product_sequence,
                'product_name': group_product_id.name,
                'purchase_unit': ' ',
                'order': ' ',
                'detail': ' ',
                'number_of_package': ' ',
                'lot_number': ' ',
                'weight': ' ',
                'note': ' ',
                'len_export_card': 0,
            }
            list.append(list_id)
            warehouse_sequence = 0
            product_ids = self.env['vnitpro.product'].search([('product_group_id', '=', group_product_id.id)])
            for warehouse_id in warehouse_ids:
                warehouse_sequence += 1
                list_id = {
                    'sequence': str(group_product_sequence) + '.' + str(warehouse_sequence),
                    'product_name': warehouse_id.name,
                    'purchase_unit': ' ',
                    'order': ' ',
                    'detail': ' ',
                    'number_of_package': ' ',
                    'lot_number': ' ',
                    'weight': ' ',
                    'note': ' ',
                    'len_export_card': 0,
                }
                list.append(list_id)
                product_sequence = 0
                for product_id in product_ids:
                    product_sequence += 1
                    export_card_list = []
                    for export_card_id in export_card_list_ids:
                        if export_card_id.product_id == product_id and export_card_id.inventory_export_product_id.warehouse_export_id == warehouse_id and export_card_id.product_group_id == group_product_id:
                            if export_card_id.note:
                                note = export_card_id.note
                            else:
                                note = ' '
                            weight = export_card_id.present_quantity / 1000
                            export_card = {
                                'purchase_unit': export_card_id.inventory_export_product_id.order_id.customer_name,
                                'order': export_card_id.inventory_export_product_id.contract_id.name,
                                'detail': ' ',
                                'number_of_package': export_card_id.number_of_packaging,
                                'lot_number': export_card_id.lot_number,
                                'weight': base.check_number(self, weight),
                                'note': note,
                            }
                            export_card_list.append(export_card)
                    len_export_card = len(export_card_list)
                    if len(export_card_list) > 0:
                        product = {
                            'sequence': str(group_product_sequence) + '.' + str(warehouse_sequence) + '.' + str(
                                product_sequence),
                            'product_name': product_id.name,
                            'export_card_list': export_card_list,
                            'len_export_card': len_export_card,
                        }
                        list.append(product)
            list_id = {
                'sequence': str(group_product_sequence) + '.' + str(warehouse_sequence + 1),
                'product_name': 'Direct Import - Export',
                'purchase_unit': ' ',
                'order': ' ',
                'detail': ' ',
                'number_of_package': ' ',
                'lot_number': ' ',
                'weight': ' ',
                'note': ' ',
                'len_export_card': 0,
            }
            list.append(list_id)
            product_sequence = 0
            for product_id in product_ids:
                product_sequence += 1
                direct_export_card_list = []
                for direct_export_card in direct_export_card_list_ids:
                    if direct_export_card.product_id == product_id and direct_export_card.product_group_id == group_product_id:
                        if direct_export_card.note:
                            note = direct_export_card.note
                        else:
                            note = ' '
                        weight = direct_export_card.present_quantity / 1000
                        export_card = {
                            'purchase_unit': direct_export_card.direct_import_product_id.order_id.customer_name,
                            'order': direct_export_card.direct_import_product_id.contract_id.name,
                            'detail': ' ',
                            'number_of_package': direct_export_card.number_of_packaging,
                            'lot_number': direct_export_card.lot_number,
                            'weight': base.check_number(self, weight),
                            'note': note,
                        }
                        direct_export_card_list.append(export_card)
                    len_direct_export_card = len(direct_export_card_list)
                    if len(direct_export_card_list) > 0:
                        product = {
                            'sequence': str(group_product_sequence) + '.' + str(warehouse_sequence) + '.' + str(
                                product_sequence),
                            'product_name': product_id.name,
                            'export_card_list': direct_export_card_list,
                            'len_export_card': len_direct_export_card,
                        }
                        list.append(product)
        return list

    def get_time(self, time):
        time = datetime.strptime(time, '%Y-%m-%d')
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        return time

    def get_date(self, data):
        start_date = self.get_time(data['start_date'])
        end_date = self.get_time(data['end_date'])
        data = {}
        data.update({'start_date': start_date,
                     'end_date': end_date})
        return data

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
            'get_data': self.get_data,
            'get_date': self.get_date,
        }
        return docargs
