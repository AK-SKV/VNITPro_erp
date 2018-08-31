# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class DeliveryUnit(models.Model):
    _name = "vnitpro.delivery.unit"
    _inherit = "vnitpro.base.information"
