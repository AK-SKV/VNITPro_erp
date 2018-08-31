# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class InspectionUnit(models.Model):
    _name = "vnitpro.inspection.unit"
    _inherit = "vnitpro.base.information"
