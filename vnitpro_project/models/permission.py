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


class Project(models.Model):
    _inherit = 'vnitpro.project'

    permission_detail_ids = fields.One2many('vnitpro.project.permission', 'project_id', 'Permission Detail')


class PermissionProject(models.Model):
    _name = 'vnitpro.project.permission'
    _inherit = 'vnitpro.base.permission'

    project_id = fields.Many2one('vnitpro.project', 'Project', required=True, ondelete="cascade")

    @api.model
    def create(self, vals):
        record = super(PermissionProject, self).create(vals)
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
            Utils.send_notify_permission(record=record.project_id,
                                         user_id=vals['user_id'],
                                         xml_id_act_window='act_open_vnitpro_project_view',
                                         task=task,
                                         message=message)
        return record

    @api.multi
    def write(self, vals):
        result = super(PermissionProject, self).write(vals)
        if result:
            task = 'Assign'
            message = ''
            if self.perm_read:
                message += ' [read permission]'
            if self.perm_write:
                message += ' [write permission]'
            if self.perm_unlink:
                message += ' [unlink permission]'
            Utils.send_notify_permission(record=self.project_id,
                                         user_id=self.user_id.id,
                                         xml_id_act_window='act_open_vnitpro_project_view',
                                         task=task,
                                         message=message)
        return result

    @api.multi
    def unlink(self):
        record = self.project_id
        user_id = self.user_id.id
        result = super(PermissionProject, self).unlink()
        if result:
            Utils.send_notify_permission(record=record,
                                         user_id=user_id,
                                         is_delete_perm=True)
        return result
