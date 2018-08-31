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
import time
import logging

_logger = logging.getLogger(__name__)

STATUS = [('completed_procurement', 'Completed Procurement'),
          ('incomplete_procurement', 'Incomplete Procurement'),
          ('unapproved_procurement_plan', 'Unapproved Procurement Plan'),
          ('not_create_procurement_advisory', 'Not Create Procurement Advisory'),
          ('not_create_invitation_pq_doc', 'Not Create Invitation PQ Document'),
          ('unapproved_pq_document', 'Unapproved PQ Document'),
          ('not_confirm_prequalification_list', 'Not Confirm Prequalification List'),
          ('not_create_bidding_document', 'Not Create Bidding Document'),
          ('unset_bidding_profile', 'Unset Bidding Profile'),
          ('no_bidding_results', 'No Bidding Results'),
          ('no_negotiation_results', 'No Negotiation Results'),
          ('no_expertise_bidder_selection', 'No Expertise Bidder Selection')]


class DashboardProcurement(models.Model):
    _name = 'vnitpro.procurement.dashboard'

    name = fields.Char('Name', compute="_compute_by_status", translate=True, store=True)
    status = fields.Selection(STATUS, 'Status', required=True)
    color = fields.Integer('Color', default=4)
    count_record = fields.Integer('Count Record', compute="_compute_count_status")
    count_expire_today = fields.Integer('Count Expire Today', compute="_compute_count_status")
    count_out_of_date = fields.Integer('Count Out Of Date', compute="_compute_count_status")
    count_unexpired = fields.Integer('Count Unexpired', compute="_compute_count_status")

    @api.model
    def load_views(self, views, options=None):
        _logger.warning(views)
        _logger.warning(options)
        return super(DashboardProcurement, self).load_views(views, options)

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
        if self.status == 'completed_procurement':
            context = {'search_default_completed_procurement': 1}
        elif self.status == 'incomplete_procurement':
            context = {'search_default_incomplete_procurement': 1}
        elif self.status == 'unapproved_procurement_plan':
            context = {'search_default_unapproved_procurement_plan': 1}
        elif self.status == 'not_create_procurement_advisory':
            context = {'search_default_not_create_procurement_advisory': 1}
        elif self.status == 'not_create_invitation_pq_doc':
            context = {'search_default_not_create_invitation_pq_doc': 1}
        elif self.status == 'unapproved_pq_document':
            context = {'search_default_not_create_pq_document': 1}
        elif self.status == 'not_confirm_prequalification_list':
            context = {'search_default_not_confirm_prequalification_list': 1}
        elif self.status == 'not_create_bidding_document':
            context = {'search_default_not_create_bidding_document': 1}
        elif self.status == 'unset_bidding_profile':
            context = {'search_default_unset_bidding_profile': 1}
        elif self.status == 'no_bidding_results':
            context = {'search_default_no_bidding_results': 1}
        elif self.status == 'no_negotiation_results':
            context = {'search_default_no_negotiation_results': 1}
        else:
            context = {'search_default_no_expertise_bidder_selection': 1}
        return context

    def get_action_procurement_with_status(self):
        context = self.get_context_with_status()
        return {
            'name': self.display_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vnitpro.procurement',
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
            'res_model': 'vnitpro.procurement',
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
            'res_model': 'vnitpro.procurement',
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
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': str(context)
        }

    @api.one
    @api.depends('status')
    def _compute_count_status(self):
        time = self.get_today()
        domains = []
        if self.status == 'completed_procurement':
            domains = [('confirmed_procurement', '=', True),
                       ('created_advision', '=', True),
                       ('created_invitation_pq_doc', '=', True),
                       ('finished_to_approve_pq_document', '=', True),
                       ('finished_to_comfirm_prequalification', '=', True),
                       ('created_bidding_document', '=', True),
                       ('finished_to_take_bid_profile', '=', True),
                       ('completed_import_bidding_results', '=', True),
                       ('completed_import_negotiation_list', '=', True),
                       ('completed_expertise_bidder_selection', '=', True)]
        elif self.status == 'incomplete_procurement':
            domains = ['|', '|', '|', '|', '|', '|', '|', '|', '|',
                       ('confirmed_procurement', '=', False),
                       ('created_advision', '=', False),
                       ('created_invitation_pq_doc', '=', False),
                       ('finished_to_approve_pq_document', '=', False),
                       ('finished_to_comfirm_prequalification', '=', False),
                       ('created_bidding_document', '=', False),
                       ('finished_to_take_bid_profile', '=', False),
                       ('completed_import_bidding_results', '=', False),
                       ('completed_import_negotiation_list', '=', False),
                       ('completed_expertise_bidder_selection', '=', False)]
        elif self.status == 'unapproved_procurement_plan':
            domains = [('confirmed_procurement', '=', False)]
        elif self.status == 'not_create_procurement_advisory':
            domains = [('created_advision', '=', False)]
        elif self.status == 'not_create_invitation_pq_doc':
            domains = [('created_invitation_pq_doc', '=', False)]
        elif self.status == 'unapproved_pq_document':
            domains = [('finished_to_approve_pq_document', '=', False)]
        elif self.status == 'not_confirm_prequalification_list':
            domains = [('finished_to_comfirm_prequalification', '=', False)]
        elif self.status == 'not_create_bidding_document':
            domains = [('created_bidding_document', '=', False)]
        elif self.status == 'unset_bidding_profile':
            domains = [('finished_to_take_bid_profile', '=', False)]
        elif self.status == 'no_bidding_results':
            domains = [('completed_import_bidding_results', '=', False)]
        elif self.status == 'no_negotiation_results':
            domains = [('completed_import_negotiation_list', '=', False)]
        elif self.status == 'no_expertise_bidder_selection':
            domains = [('completed_expertise_bidder_selection', '=', False)]
        self.count_expire_today = len(self.env['vnitpro.procurement'].search(
            domains + [('expire_date', '=', time)]))
        self.count_unexpired = len(self.env['vnitpro.procurement'].search(
            domains + [('expire_date', '>', time)]))
        self.count_out_of_date = len(self.env['vnitpro.procurement'].search(
            domains + [('expire_date', '<', time)]))
        self.count_record = self.count_expire_today + self.count_unexpired + self.count_out_of_date

    @api.one
    @api.depends('status')
    def _compute_by_status(self):
        self.name = dict(self._fields['status'].selection).get(self.status)
