# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class DeliveryFormality(models.Model):
    _name = "vnitpro.delivery.formality"
    _inherit = "vnitpro.base.information"
