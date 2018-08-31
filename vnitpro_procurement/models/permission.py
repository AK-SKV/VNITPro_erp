# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api
from odoo.addons.vnitpro_base.models.utils import Utils
import logging

_logger = logging.getLogger(__name__)


class Procurement(models.Model):
    _inherit = 'vnitpro.procurement'

    permission_detail_ids = fields.One2many(
        'vnitpro.procurement.permission', 'procurement_id', 'Procurement Detail')


class ResUser(models.Model):
    _inherit = 'res.users'
    procurement_permission_ids = fields.One2many(
        'vnitpro.procurement.permission', 'user_id', 'Procurement Permission')


class PermissionProcurement(models.Model):
    _name = 'vnitpro.procurement.permission'
    _inherit = 'vnitpro.base.permission'

    employee_id = fields.Many2one('vnitpro.employee', 'Employee', required=True,
                                  domain=lambda self: self._domain_employee())
    user_id = fields.Many2one('res.users', 'User', related="employee_id.res_user_id", store=True)
    procurement_id = fields.Many2one(
        'vnitpro.procurement', 'Procurement', required=True, ondelete="cascade")

    _sql_constraints = [('unique_procurement_employee', 'unique(procurement_id,employee_id)',
                         'Employee must be unique in permission of procurement table')]

    def _domain_employee(self):
        domain = []
        group_procurement = self.env.ref('vnitpro_procurement.group_procurement', False)
        if group_procurement != None:
            group_procurement_id = self.env['res.groups'].browse([group_procurement.id])
            domain += [('res_user_id', 'in', group_procurement_id.users.ids),
                       ('res_user_id', '!=', self.env.uid)]
        _logger.warning(domain)
        return domain

    @api.model
    def create(self, vals):
        record = super(PermissionProcurement, self).create(vals)
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
            Utils.send_notify_permission(record=record.procurement_id,
                                         user_id=vals['user_id'],
                                         xml_id_act_window='act_open_vnitpro_procurement_view',
                                         task=task,
                                         message=message)
        return record

    @api.multi
    def write(self, vals):
        result = super(PermissionProcurement, self).write(vals)
        if result:
            task = 'Assign'
            message = ''
            if self.perm_read:
                message += ' [read permission]'
            if self.perm_write:
                message += ' [write permission]'
            if self.perm_unlink:
                message += ' [unlink permission]'
            Utils.send_notify_permission(record=self.procurement_id,
                                         user_id=self.user_id.id,
                                         xml_id_act_window='act_open_vnitpro_procurement_view',
                                         task=task,
                                         message=message)
        return result

    @api.multi
    def unlink(self):
        record = self.procurement_id
        user_id = self.user_id.id
        result = super(PermissionProcurement, self).unlink()
        if result:
            Utils.send_notify_permission(record=record,
                                         user_id=user_id,
                                         is_delete_perm=True)
        return result
