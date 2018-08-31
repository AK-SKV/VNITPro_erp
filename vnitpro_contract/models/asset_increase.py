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


# # author: Tu Vo, model: .py, model asset_increase
# # tác giả: Võ Tuấn Tú, model: asset_increase.py, model tăng tài sản

class AssetIncrease(models.Model):
    _name = 'vnitpro.asset.increase'

    # contract sub information
    contract_id = fields.Many2one('vnitpro.contract', 'Contract', ondelete='cascade')
    bidder_a = fields.Many2one("vnitpro.bidder", "Bidder A", related='contract_id.bidder_a', store=True, readonly=True)
    bidder_b = fields.Many2one("vnitpro.bidder", "Bidder B", related='contract_id.bidder_b', store=True, readonly=True)
    receiver = fields.Char('Receiver', required=True, track_visibility='onchange')
    sender = fields.Char('Sender', required=True, track_visibility='onchange')
    asset_type = fields.Many2one('vnitpro.asset.type', 'Asset Type', required=True, track_visibility='onchange',
                                 domain="[('activate','=','usage')]")
    price = fields.Float('Asset Price', required=True, digits=(3, 2), track_visibility='onchange')
    increase_date = fields.Date('Increase Date', required=True, track_invisibility='onchange')
    note = fields.Text('Description', track_visibility='onchange')
    file_attachment_ids = fields.One2many('vnitpro.base.attachment', 'asset_increase_id', 'Attach File')

    @api.multi
    @api.constrains('price')
    def constrains(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError(_("Asset price have to higher than 0!"))
