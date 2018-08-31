# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Bidder(models.Model):
    _name = "vnitpro.bidder"
    _inherit = "vnitpro.base.information"

    phone_number = fields.Char('Phone number', size=300)
    address = fields.Char('Address', size=300)
    tax_code = fields.Char('Tax code', size=300)
    fax = fields.Char('Fax', size=300)
    description = fields.Text('Note', size=900)
    representative = fields.Char('Representative', size=300)
    phone_number_representative = fields.Char('Phone number of representative', size=300)
    representative_position = fields.Char('Representative position', size=300)
    representative_email = fields.Char('Representative email', size=300)
    bank_of_bidder_ids = fields.One2many('vnitpro.bank.of.bidder', 'bidder_id')
    # bank_numbers = fields.Integer('Bank Numbers', compute="count_bank_numbers", store=True)

    # @api.multi
    # @api.depends('bank_of_bidder_ids')
    # def count_bank_numbers(self):
    #     for record in self:
    #         record.bank_numbers = len(record.bank_of_bidder_ids)

    # @api.multi
    # @api.constrains('bank_numbers')
    # def constrains_bank_numbers(self):
    #     for record in self:
    #         _logger.warning('oke')
    #         if record.bank_numbers == 0:
    #             _logger.warning('dieeee')
    #             raise ValidationError(_('Bank must be required !'))
