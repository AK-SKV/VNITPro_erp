# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Created by: tam.pt
###############################################################################

from odoo import models, fields, api, _


class BasePermission(models.Model):
    _name = 'vnitpro.base.permission'

    user_id = fields.Many2one('res.users', 'User', required=True)
    perm_read = fields.Boolean('Read permission', default=False)
    perm_write = fields.Boolean('Write permission', default=False)
    perm_unlink = fields.Boolean('Delete permission', default=False)

    @api.multi
    def write(self, vals):
        result = super(BasePermission, self).write(vals)
        self.env['ir.rule'].clear_caches()
        return result

    @api.multi
    def unlink(self):
        result = super(BasePermission, self).unlink()
        self.env['ir.rule'].clear_caches()
        return result

    @api.model
    def create(self, vals):
        result = super(BasePermission, self).create(vals)
        self.env['ir.rule'].clear_caches()
        return result
