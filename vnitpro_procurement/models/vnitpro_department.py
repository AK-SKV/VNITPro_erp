# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class Department(models.Model):
    _inherit = 'vnitpro.department'

    permission_approve = fields.Boolean('Approve Permission')
