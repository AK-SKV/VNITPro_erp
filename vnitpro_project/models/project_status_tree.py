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

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "vnitpro.project"

    status_tree = fields.Text('Status', size=200, compute='compute_status_tree')

    @api.one
    @api.depends('expire_date', 'confirm_status', 'status')
    def compute_status_tree(self):
        msg = ''
        if self.confirm_status == 1:
            msg += _('- Project Draft\n')
        if self.confirm_status == 2:
            msg += _('- Project Confirmed\n')
        # (2, 'Pending'), (3, 'In Process'), (4, 'Finish'), (5, 'On Hold'), (6, 'Cancel')
        if self.status == 3:
            msg += _('- In Process Project\n')
        if self.status == 4:
            msg += _('- Finish Project\n')
        if self.status == 5:
            msg += _('- On Hold Project\n')
        if self.status == 6:
            msg += _('- Cancel Project\n')
        if self.expire_date:
            time = datetime.datetime.now()
            tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
            tz_database = pytz.timezone('UTC')
            time = tz_database.localize(time)
            time = time.astimezone(tz_current)
            time = time.date()
            expire_date = datetime.datetime.strptime(self.expire_date, '%Y-%m-%d')
            days = (expire_date.date() - time).days
            if days < 0 and self.status not in [4, 6]:
                msg += _('- Out of date: %d day(s)') % abs(days)
            elif days > 0 and self.status not in [4, 6]:
                msg += _('- %d day(s) left') % abs(days)
            elif self.status not in [4, 6]:
                msg += _('- Expire Today')
        self.status_tree = msg
