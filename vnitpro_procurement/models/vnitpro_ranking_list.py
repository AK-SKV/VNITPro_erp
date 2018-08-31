# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

RESULT = [(1, 'Passed'), (2, 'Not Passed')]


class Procurement(models.Model):
    _inherit = "vnitpro.procurement"

    ranking_list_ids = fields.One2many('vnitpro.ranking.list', 'procurement_id', 'Ranking List')
    completed_import_bidding_results = fields.Boolean('Completed Import Bidding Results')


class RankingList(models.Model):
    _name = "vnitpro.ranking.list"
    _rec_name = 'bid_profile_id'

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', required=True, ondelete="cascade")
    bid_profile_id = fields.Many2one('vnitpro.bid.profile', 'Bid Profile', required=True)
    point = fields.Float('Point', size=50, digits=(3, 2), required=True)
    date_of_bid = fields.Date('Date Of Bid', track_visibility="onchange", required=True)
    the_price_includes_vat = fields.Float('The Price Includes VAT', size=50, digits=(3, 2), required=True)
    discount = fields.Float('Discount', size=50, digits=(3, 2))
    expertise_team_leader = fields.Many2one('vnitpro.employee', 'Expertise Team Leader',
                                            domain="[('activate','=','usage')]", required=True)
    expertise_team_member = fields.Many2one('vnitpro.employee', 'Expertise Team Member',
                                            domain="[('activate','=','usage')]")
    expert_team_leader = fields.Many2one('vnitpro.employee', 'Expert Team Leader', domain="[('activate','=','usage')]",
                                         required=True)
    expert_team_member = fields.Many2one('vnitpro.employee', 'Expert Team Member', domain="[('activate','=','usage')]")
    result = fields.Selection(RESULT, 'Result', required=True, default=1)
    review_and_note = fields.Text('Review and note', size=500)
    attachment_ids = fields.One2many('vnitpro.base.attachment', 'ranking_list_id', 'Attach Files')

    _sql_constraints = [
        ('unique_bid_profile_id_procurement_id', 'unique(procurement_id,bid_profile_id)',
         'Bid Profile must be unique per ranking list !')
    ]

    @api.one
    @api.constrains('point')
    def validate_point(self):
        if self.point < 0:
            raise ValidationError(_('Point must be bigger than 0 !'))

    @api.multi
    @api.constrains('the_price_includes_vat')
    def validate_the_price_includes_vat(self):
        for record in self:
            if record.the_price_includes_vat <= 0:
                raise ValidationError(_('The Price Includes VAT must be bigger than 0 !'))

    @api.one
    @api.constrains('discount')
    def validate_discount(self):
        if self.discount < 0:
            raise ValidationError(_('Discount must be bigger than 0 !'))


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    ranking_list_id = fields.Many2one('vnitpro.ranking.list', 'Ranking List', ondelete='cascade')
