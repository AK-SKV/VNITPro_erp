# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, api, fields, _


class Unit(models.Model):
    _name = 'vnitpro.unit'
    _inherit = 'vnitpro.base.information'
