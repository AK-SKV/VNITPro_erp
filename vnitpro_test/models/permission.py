# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class Testpermission(models.Model):
    _name = "vnitpro.test.permission"

    test_id = fields.Many2one('vnitpro.test', 'Test', required=True)
    user_id = fields.Many2one('res.users', 'User', required=True)
    perm_read = fields.Boolean('Read')
    perm_create = fields.Boolean('Create')
    perm_write = fields.Boolean('Write')
    perm_delete = fields.Boolean('Delete')

    @api.model
    def create(self, vals):
        record = super(Testpermission, self).create(vals)
        try:
            if 'user_id' in vals:
                name = 'groups_%s' % (vals['user_id'])
                group = self.env['res.groups'].search([('name', '=', name)], limit=1)
                if len(group) == 0:
                    group = self.env['res.groups'].create({'name': name})
                group[0].users = [(4, vals['user_id'])]

                model_id = self.env['ir.model'].search([('model', '=', 'vnitpro.test')], limit=1).id
                # model_access = self.env['ir.model.access'].search(
                #     [('model_id', '=', model_id), ('group_id', '=', group.id), ('name', '=', 'vnitpro.test_read')], limit=1)
                # if len(model_access) == 0:
                #     model_access = self.env['ir.model.access'].create({'name': 'vnitpro.test_read',
                #                                                        'model_id': model_id,
                #                                                        'group_id': group.id,
                #                                                        'perm_read': True,
                #                                                        'perm_write': False,
                #                                                        'perm_create': False,
                #                                                        'perm_unlink': False,
                #                                                        'active': True})
                model_access = self.env['ir.model.access'].search(
                    [('model_id', '=', model_id), ('group_id', '=', group.id), ('name', '=', 'vnitpro.test_create')], limit=1)
                if len(model_access) == 0:
                    model_access = self.env['ir.model.access'].create({'name': 'vnitpro.test_create',
                                                                       'model_id': model_id,
                                                                       'group_id': group.id,
                                                                       'perm_read': False,
                                                                       'perm_write': False,
                                                                       'perm_create': True,
                                                                       'perm_unlink': False,
                                                                       'active': True})

                # rule = self.env['ir.rule'].search(
                #     [('model_id', '=', model_id), ('name', '=', 'vnitpro.test_read')], limit=1)
                # if len(rule) == 0:
                #     rule = self.env['ir.rule'].create({'name': 'vnitpro.test_read',
                #                                        'model_id': model_id,
                #                                        'domain_force': '[(\'permission_ids.user_id\',\'=\',user.id)]',
                #                                        'perm_read': True,
                #                                        'perm_write': False,
                #                                        'perm_create': False,
                #                                        'perm_unlink': False,
                #                                        'global': False})
                # group[0].rule_groups = [(4, rule.id)]

                rule = self.env['ir.rule'].search(
                    [('model_id', '=', model_id), ('name', '=', 'vnitpro.test_create')], limit=1)
                if len(rule) == 0:
                    rule = self.env['ir.rule'].create({'name': 'vnitpro.test_create',
                                                       'model_id': model_id,
                                                       'domain_force': '[(\'permission_ids.user_id\',\'=\',user.id)]',
                                                       'perm_read': False,
                                                       'perm_write': False,
                                                       'perm_create': True,
                                                       'perm_unlink': False,
                                                       'global': False})
                group[0].rule_groups = [(4, rule.id)]
        except:
            pass
        return record
