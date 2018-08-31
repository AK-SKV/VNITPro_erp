# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re, logging, datetime

_logger = logging.getLogger(__name__)


class ContractDashboard(models.Model):
    _name = 'vnitpro.contract.dashboard'

    name = fields.Char('Name', compute='compute_name', store=True)
    status = fields.Selection([('pending', 'Pending'),
                               ('in_process', 'In Process'),
                               ('asset_increase', 'Asset Increase'),
                               ('acceptance_payment', 'Acceptance - Payment'),
                               ('liquidated_finalized', 'Liquidated - Finalized'),
                               ('on_hold', 'On Hold'),
                               ('cancel', 'Cancel')], 'Status', required=True)
    color = fields.Integer()
    count_pending_contract = fields.Integer(compute='_compute_count_contract')
    count_in_process_contract = fields.Integer(compute='_compute_count_contract')
    count_asset_increase_contract = fields.Integer(compute='_compute_count_contract')
    count_acceptance_payment_contract = fields.Integer(compute='_compute_count_contract')
    count_liquidated_finalized_contract = fields.Integer(compute='_compute_count_contract')
    count_on_hold_contract = fields.Integer(compute='_compute_count_contract')
    count_cancel_contract = fields.Integer(compute='_compute_count_contract')
    count_late_contract = fields.Integer(compute='_compute_count_contract')
    count_today_contract = fields.Integer(compute='_compute_count_contract')
    count_soon_expired_contract = fields.Integer(compute='_compute_count_contract')
    count_during_contract = fields.Integer(compute='_compute_count_contract')
    count_guarantee_contract = fields.Integer(compute='_compute_count_contract')
    count_warranty_contract = fields.Integer(compute='_compute_count_contract')
    count_guarantee_warranty_contract = fields.Integer(compute='_compute_count_contract')

    def _get_action(self, action_xmlid):
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.display_name
        return action

    def get_action_contract(self):
        return self._get_action('vnitpro_contract.act_contract')

    def get_action_late_contract(self):
        return self._get_action('vnitpro_contract.act_late_contract')

    def get_action_today_contract(self):
        return self._get_action('vnitpro_contract.act_today_contract')

    def get_action_soon_expired_contract(self):
        return self._get_action('vnitpro_contract.act_soon_expired_contract')

    def get_action_during_contract(self):
        return self._get_action('vnitpro_contract.act_during_contract')

    def get_action_guarantee_contract(self):
        return self._get_action('vnitpro_contract.act_guarantee_contract')

    def get_action_warranty_contract(self):
        return self._get_action('vnitpro_contract.act_warranty_contract')

    @api.one
    @api.depends('status')
    def _compute_count_contract(self):
        if self.status == 'pending':
            self.count_pending_contract = len(self.env['vnitpro.contract'].search([('status', '=', 'pending')]))
        elif self.status == 'in_process':
            self.count_late_contract = len(
                self.env['vnitpro.contract'].search(
                    [('status', '=', 'in_process'), ('expire_date', '<', datetime.date.today())]))
            self.count_today_contract = len(
                self.env['vnitpro.contract'].search(
                    [('status', '=', 'in_process'), ('expire_date', '=', datetime.date.today())]))
            self.count_soon_expired_contract = len(self.env['vnitpro.contract'].search(
                [('status', '=', 'in_process'), ('expire_date', '>', datetime.date.today()), ('day_left', '=', 1)]))
            self.count_during_contract = len(self.env['vnitpro.contract'].search(
                [('status', '=', 'in_process'), ('expire_date', '>', datetime.date.today())]))
            self.count_in_process_contract = len(self.env['vnitpro.contract'].search([('status', '=', 'in_process')]))
            self.count_guarantee_contract = len(self.env['vnitpro.contract'].search(
                [('warning', '=', 'guarantee_expire'), ('status', '=', 'in_process')]))
            self.count_warranty_contract = len(self.env['vnitpro.contract'].search(
                [('warning', '=', 'warranty_expire'), ('status', '=', 'in_process')]))
            self.count_guarantee_warranty_contract = len(self.env['vnitpro.contract'].search(
                [('warning', '=', 'guarantee_warranty_expire'), ('status', '=', 'in_process')]))
        elif self.status == 'asset_increase':
            self.count_asset_increase_contract = len(
                self.env['vnitpro.contract'].search([('status', '=', 'asset_increase')]))
        elif self.status == 'acceptance_payment':
            self.count_acceptance_payment_contract = len(
                self.env['vnitpro.contract'].search([('status', '=', 'acceptance_payment')]))
        elif self.status == 'liquidated_finalized':
            self.count_liquidated_finalized_contract = len(
                self.env['vnitpro.contract'].search([('status', '=', 'liquidated_finalized')]))
        elif self.status == 'on_hold':
            self.count_on_hold_contract = len(self.env['vnitpro.contract'].search([('status', '=', 'on_hold')]))
        elif self.status == 'cancel':
            self.count_cancel_contract = len(self.env['vnitpro.contract'].search([('status', '=', 'cancel')]))

    @api.one
    @api.depends('status')
    def compute_name(self):
        if self.status == 'pending':
            self.name = _('Pending')
        elif self.status == 'in_process':
            self.name = _('In Process')
        elif self.status == 'asset_increase':
            self.name = _('Asset Increase')
        elif self.status == 'acceptance_payment':
            self.name = _('Acceptance Payment')
        elif self.status == 'liquidated_finalized':
            self.name = _('Liquidated Finalized')
        elif self.status == 'on_hold':
            self.name = _('On Hold')
        elif self.status == 'cancel':
            self.name = _('Cancel')
