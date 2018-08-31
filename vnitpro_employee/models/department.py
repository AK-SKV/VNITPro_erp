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


class Department(models.Model):
    _name = 'vnitpro.department'
    _inherit = 'vnitpro.base.information'
    _desciption = 'Department'

    employee_ids = fields.One2many('vnitpro.employee', 'department_id', 'Employees')
    count_employee = fields.Integer('Count Employee', compute="_compute_count_employee")
    color = fields.Integer('Color', default=3)

    @api.multi
    @api.depends('employee_ids')
    def _compute_count_employee(self):
        for record in self:
            _logger.warning(len(record.employee_ids))
            record.count_employee = len(record.employee_ids)

    def _get_action(self, action_xmlid):
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.display_name
        return action

    def get_action_employee_in_department(self):
        return self._get_action('vnitpro_employee.act_open_vnitpro_employee_in_department_view')
