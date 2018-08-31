# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)


class LandAssessCategory(models.Model):
    _name = 'vnitpro.assess.category'
    _inherit = 'vnitpro.base.information', 'mail.thread'
    _description = 'Assess Category'
