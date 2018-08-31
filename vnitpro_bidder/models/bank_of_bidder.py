# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#    Create by tam.pt
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BankOfBidder(models.Model):
    _name = "vnitpro.bank.of.bidder"

    bidder_id = fields.Many2one('vnitpro.bidder', 'Bidder',
                                domain="[('activate','=', 'usage')]", ondelete="cascade", required=True)
    account_number = fields.Char('Account number', size=300)
    bank_id = fields.Many2one('vnitpro.bank', 'Bank', required=True, domain="[('activate','=', 'usage')]")
    branch = fields.Char('Branch', size=300)

    _sql_constraints = [('unique_account_number', 'unique(account_number)',
                         'The account number already exists, please try another.')]
