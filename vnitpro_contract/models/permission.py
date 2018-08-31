# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api
import logging
from odoo.addons.vnitpro_base.models.utils import Utils

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = 'vnitpro.contract'

    permission_detail_ids = fields.One2many(
        'vnitpro.contract.permission', 'contract_id', 'Permission Detail')


class ResUser(models.Model):
    _inherit = 'res.users'
    contract_permission_ids = fields.One2many(
        'vnitpro.contract.permission', 'user_id', 'Contract Permission')


class PermissionContract(models.Model):
    _name = 'vnitpro.contract.permission'
    _inherit = 'vnitpro.base.permission'

    employee_id = fields.Many2one('vnitpro.employee', 'Employee', required=True,
                                  domain=lambda self: self._domain_employee())
    user_id = fields.Many2one('res.users', 'User', related="employee_id.res_user_id", store=True)
    contract_id = fields.Many2one('vnitpro.contract', 'Contract',
                                  required=True, ondelete="cascade")

    _sql_constraints = [('unique_contract_employee', 'unique(contract_id,employee_id)',
                         'Employee must be unique in permission of contract table')]

    def _domain_employee(self):
        domain = []
        group_contract = self.env.ref('vnitpro_contract.group_contract', False)
        if group_contract != None:
            group_contract_id = self.env['res.groups'].browse([group_contract.id])
            domain += [('res_user_id', 'in', group_contract_id.users.ids),
                       ('res_user_id', '!=', self.env.uid)]
        return domain

    @api.model
    def create(self, vals):
        record = super(PermissionContract, self).create(vals)
        if record:
            perm_read = vals['perm_read']
            perm_write = vals['perm_write']
            perm_unlink = vals['perm_unlink']
            task = 'Assign'
            message = ''
            if perm_read:
                message += ' [read permission]'
            if perm_write:
                message += ' [write permission]'
            if perm_unlink:
                message += ' [unlink permission]'
            Utils.send_notify_permission(record=record.contract_id,
                                         user_id=vals['user_id'],
                                         xml_id_act_window='act_open_vnitpro_contract_view',
                                         task=task,
                                         message=message)
        return record

    @api.multi
    def write(self, vals):
        result = super(PermissionContract, self).write(vals)
        if result:
            task = 'Assign'
            message = ''
            if self.perm_read:
                message += ' [read permission]'
            if self.perm_write:
                message += ' [write permission]'
            if self.perm_unlink:
                message += ' [unlink permission]'
            Utils.send_notify_permission(record=self.contract_id,
                                         user_id=self.user_id.id,
                                         xml_id_act_window='act_open_vnitpro_contract_view',
                                         task=task,
                                         message=message)
        return result

    @api.multi
    def unlink(self):
        record = self.contract_id
        user_id = self.user_id.id
        result = super(PermissionContract, self).unlink()
        if result:
            Utils.send_notify_permission(record=record,
                                         user_id=user_id,
                                         is_delete_perm=True)
        return result
