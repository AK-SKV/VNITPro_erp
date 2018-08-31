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


class ReportInventoryList(models.AbstractModel):
    _name = "report.vnitpro_inventory.report_gen_import_product"

    def get_title_report(self):
        data = {}
        time = datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current).strftime(_('%m-%d-%Y'))
        time = _('Report Date: ') + time
        title_report = _('Import Product Report')
        data.update({'time_report': time, 'title_report': title_report})
        return data

    def get_data(self, data):
        import_card_list_ids = self.env['vnitpro.inventory.import.product.detail'].browse(data['import_card_ids'])
        import_formality_standard_ids = self.env['vnitpro.inventory.import.formality.product.standard'].search([])
        import_formality_defects_ids = self.env['vnitpro.inventory.import.formality.product.defects'].search([])
        warehouse_ids = self.env['vnitpro.warehouse'].search([])
        list = []
        _logger.warning(import_formality_standard_ids)

        title_standard = []
        for import_formality in import_formality_standard_ids:
            title = import_formality.name
            list_id ={
                'title':title
            }
            title_standard.append(list_id)
        title_defects = []
        for import_formality in import_formality_defects_ids:
            title = import_formality.name
            list_id = {
                'title': title
            }
            title_defects.append(list_id)
        list_id={
            'title_standard':title_standard,
            'title_defects':title_defects,
            'len_title_standard':len(import_formality_standard_ids)*2,
            'len_title_defects':len(import_formality_defects_ids)*2,
        }
        _logger.warning(len(import_formality_standard_ids)*2)
        list.append(list_id)
        return list

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
        }
        return docargs
