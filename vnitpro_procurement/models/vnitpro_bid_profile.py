# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    bid_profile_ids = fields.One2many('vnitpro.bid.profile', 'procurement_id', 'Bid profile/Offer Profile')
    finished_to_take_bid_profile = fields.Boolean('Finished To Take Bid Profile')


class BidProfile(models.Model):
    _name = "vnitpro.bid.profile"
    _inherit = "vnitpro.approve.pq.document"

    attachment_ids = fields.One2many('vnitpro.base.attachment', 'bid_profile_id', 'Attach Files')

    @api.one
    @api.depends('before_tax', 'vat_confirm')
    def compute_rec_name(self):
        self.money_tax = self.before_tax * self.vat_confirm / 100


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    bid_profile_id = fields.Many2one('vnitpro.bid.profile', 'Bid profile/Offer Profile', ondelete='cascade')
