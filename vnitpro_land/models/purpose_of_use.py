# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _


class PurposeOfUse(models.Model):
    _name = 'vnitpro.purpose.of.use'
    _inherit = 'mail.thread', 'vnitpro.base.information'
