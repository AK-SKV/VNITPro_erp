# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
import datetime
import pytz
import logging
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    status_tree = fields.Text('Status', size=200, compute='compute_status_tree')

    @api.one
    @api.depends('expire_date', 'finished_to_approve_pq_document', 'completed_import_bidding_results',
                 'finished_to_take_bid_profile', 'confirmed_bidding_document', 'finished_to_comfirm_prequalification',
                 'completed_expertise_bidder_selection', 'approved',
                 'completed_import_negotiation_list', 'confirmed', 'confirmed_procurement')
    def compute_status_tree(self):
        msg = ''
        if self.confirmed_procurement == False:
            msg += _('- Unapproved Procurement Plan\n')
        if self.created_advision == False:
            msg += _('- Not Create Procurement Advisory \n')
        if self.created_invitation_pq_doc == False:
            msg += _('- Not Create Invitation PQ Document \n')
        if self.finished_to_approve_pq_document == False:
            msg += _('- Unapproved PQ Document \n')
        if self.finished_to_comfirm_prequalification == False:
            msg += _('- Not Confirm Prequalification List \n')
        if self.created_bidding_document == False:
            msg += _('- Not Create Bidding Document \n')
        if self.finished_to_take_bid_profile == False:
            msg += _('- Unset Bidding Profile \n')
        if self.completed_import_bidding_results == False:
            msg += _('- No Bidding Results \n')
        if self.completed_import_negotiation_list == False:
            msg += _('- No Negotiation Results \n')
        if self.completed_expertise_bidder_selection == False:
            msg += _('- No Expertise Bidder Selection \n')
        if msg == '':
            msg += _('- Completed Procurement Profile \n')
        else:
            if self.expire_date:
                time = datetime.datetime.now()
                tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
                tz_database = pytz.timezone('UTC')
                time = tz_database.localize(time)
                time = time.astimezone(tz_current)
                time = time.date()
                expire_date = datetime.datetime.strptime(self.expire_date, '%Y-%m-%d')
                days = (expire_date.date() - time).days
                if days < 0:
                    msg += _('- Out of date: %d day(s)') % abs(days)
                elif days > 0:
                    msg += _('- %d day(s) left') % abs(days)
                else:
                    msg += _('- Expire Today')
        self.status_tree = msg
