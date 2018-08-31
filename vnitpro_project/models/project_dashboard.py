# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################
from xml.etree import ElementTree
from odoo import models, fields, api, _
import datetime
import pytz
import logging

_logger = logging.getLogger(__name__)


class DashboardProject(models.Model):
    _name = 'vnitpro.project.dashboard'

    name = fields.Char('Name', compute="_compute_by_status", translate=True, store=True)
    status = fields.Selection(
        [(1, 'Project Draft'), (2, 'Project Confirmed'), (3, 'In Process'), (4, 'Finish'), (5, 'On Hold'),
         (6, 'Cancel')], 'Status', default=1, required=True)

    color = fields.Integer('Color', default=3)

    count_record = fields.Integer('Count Record', compute="_compute_by_status")
    count_expire_today = fields.Integer('Count Expire Today', compute="_compute_by_status")
    count_out_of_date = fields.Integer('Count Out Of Date', compute="_compute_by_status")
    count_unexpired = fields.Integer('Count Unexpired', compute="_compute_by_status")

    def get_today(self):
        time = datetime.datetime.now()
        tz_current = pytz.timezone(self._context.get('tz') or 'UTC')  # get timezone user
        tz_database = pytz.timezone('UTC')
        time = tz_database.localize(time)
        time = time.astimezone(tz_current)
        today_w_timezone = time.strftime('%Y-%m-%d')
        return today_w_timezone

    def get_context_with_status(self):
        context = {}
        # (1, 'Project Draft'), (2, 'Project Confirmed'), (3, 'In Process'), (4, 'Finish'), (5, 'On Hold'), (6, 'Cancel')
        if self.status == 1:
            context = {'search_default_project_draft': 1}
        elif self.status == 2:
            context = {'search_default_project_confirmed': 1}
        elif self.status == 3:
            context = {'search_default_project_in_process': 1}
        elif self.status == 4:
            context = {'search_default_project_finish': 1}
        elif self.status == 5:
            context = {'search_default_project_on_hold': 1}
        elif self.status == 6:
            context = {'search_default_project_cancel': 1}
        return context

    def get_action_project_with_status(self):
        context = self.get_context_with_status()
        return {
            'name': self.display_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vnitpro.project',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': str(context)
        }

    def get_action_picking_tree_expire_today(self):
        context = {'search_default_expire_today': 1}
        context.update(self.get_context_with_status())
        return {
            'name': self.display_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vnitpro.project',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': str(context)
        }

    def get_action_picking_tree_unexpired(self):
        context = {'search_default_unexpired': 1}
        context.update(self.get_context_with_status())
        return {
            'name': self.display_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vnitpro.project',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': str(context)
        }

    def get_action_picking_tree_out_of_date(self):
        context = {'search_default_out_of_date': 1}
        context.update(self.get_context_with_status())
        return {
            'name': self.display_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vnitpro.project',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': str(context)
        }

    @api.one
    @api.depends('status')
    def _compute_by_status(self):
        if self.status:
            time = self.get_today()
            self.name = dict(self._fields['status'].selection).get(self.status)
            domains = []
            # (1, 'Project Draft'), (2, 'Project Confirmed'), (3, 'In Process'), (4, 'Finish'), (5, 'On Hold'), (6, 'Cancel')
            if self.status == 1:
                domains = [('status', '=', 1)]
            elif self.status == 2:
                domains = ['&', '|', '|', '|', ('status', '=', 3), ('status', '=', 4),
                           ('status', '=', 5), ('status', '=', 6), ('status', '=', 2)]
            elif self.status == 3:
                domains = [('status', '=', 3)]
            elif self.status == 4:
                domains = [('status', '=', 4)]
            elif self.status == 5:
                domains = [('status', '=', 5)]
            elif self.status == 6:
                domains = [('status', '=', 6)]
            self.count_expire_today = len(self.env['vnitpro.project'].search(
                domains + [('expire_date', '=', time)]))
            self.count_unexpired = len(self.env['vnitpro.project'].search(
                domains + [('expire_date', '>', time)]))
            self.count_out_of_date = len(self.env['vnitpro.project'].search(
                domains + [('expire_date', '<', time)]))
            self.count_record = self.count_expire_today + self.count_unexpired + self.count_out_of_date
