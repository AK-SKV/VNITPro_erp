# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _name = 'vnitpro.employee'
    _inherit = 'vnitpro.base.person'
    _desciption = 'Employee'
    _rec_name = 'display_name'

    display_name = fields.Char('Display Name', compute="_compute_display_name")
    department_id = fields.Many2one('vnitpro.department', 'Department', required=True,
                                    domain="[('activate','=', 'usage')]")
    res_user_id = fields.Many2one('res.users', 'User Account')
    position_id = fields.Many2one('vnitpro.position', 'Position')
    id_number = fields.Char('ID Number', size=20)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender', required=True)
    birthday = fields.Date('Birthday')

    _sql_constraints = [
        ('unique_res_user_id', 'unique(res_user_id)', 'User Account must be unique')
    ]

    @api.multi
    @api.depends('department_id', 'name')
    def _compute_display_name(self):
        for record in self:
            if record.department_id and record.name:
                record.display_name = record.name + ' - ' + record.department_id.code
