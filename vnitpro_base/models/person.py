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


class Person(models.Model):
    _name = "vnitpro.base.person"
    _inherit = 'vnitpro.base.information'
    _order = 'activate desc, code asc'

    image = fields.Binary('Picture', attachment=True)
    address = fields.Text('Address', size=1500)
    phone = fields.Char('Phone', size=20)
    email = fields.Char('Email', size=200)

    @api.multi
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", record.email):
                raise ValidationError(_("Email is invalid!"))

    @api.multi
    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and (
                    not re.match("^[0-9]*$", record.phone) or len(record.phone) > 12 or len(record.phone) < 9):
                raise ValidationError(_("Please Provide valid Phone."))

    @api.multi
    @api.constrains('website')
    def _check_website(self):
        for record in self:
            if record.website and not re.match("^[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9-.]+$", record.website):
                raise ValidationError(_("Website is invalid!"))
