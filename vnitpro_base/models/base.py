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
import locale
import logging
_logger = logging.getLogger(__name__)


class BaseInformation(models.AbstractModel):
    _name = "vnitpro.base.information"
    _order = 'activate desc, code asc'

    code = fields.Char('Code', size=50, required=True, track_visibility="onchange")
    name = fields.Char('Name', size=255, required=True, track_visibility="onchange")
    activate = fields.Selection([('not_used', 'Not used'), ('usage', 'Usage')],
                                'Status', required=True, default='usage')
    description = fields.Text('Description', size=900, track_visibility="onchange")

    _sql_constraints = [('unique_code', 'unique(code)', 'The code already exists, please try another.')]

    @api.multi
    @api.onchange('code')
    def change_code(self):
        for record in self:
            if record.code:
                code = record.code
                record.code = code.upper()

    @api.multi
    @api.constrains('code')
    def _compute_special_character_code(self):
        for record in self:
            if not re.match("^[a-zA-Z0-9_\-/\\\\]*$", record.code):
                raise ValidationError(_(
                    "Invalid Code, please try again ( Code only contains letters, numbers and character: / , \\ , _ ) ."))

    @api.model
    def create(self, vals):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(BaseInformation, self).create(vals)

    @staticmethod
    def check_number(self, number):
        locale.setlocale(locale.LC_ALL, '%s.UTF-8' % self.env.user.partner_id.lang)
        if int(number) == float(number):
            return locale.format('%.0f', number, 1)
        else:
            return locale.format('%.2f', number, 1)
