# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, api, fields, _


class BaseCurrency(models.Model):
    _name = 'vnitpro.currency'
    _inherit = 'vnitpro.base.information'
    _rec_name = 'code'
    _order = 'activate,id desc'
