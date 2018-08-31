# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import fields, models, api, _


class Contract(models.Model):
    _inherit = 'vnitpro.contract'

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', track_visibility="onchange")
    procurement_formality = fields.Many2one('vnitpro.procurement.formality',
                                            related="procurement_id.procurement_formality_id", readonly=True)
    cost_estimate = fields.Float(
        'Cost Estimate', related="procurement_id.vat_information", digits=(3, 2), readonly=True)
    price_plan = fields.Float('Price Plan', related="procurement_id.after_tax", digits=(3, 2), readonly=True)
    price_won_procurement = fields.Float(
        'Price Won Procurement', compute="_compute_price_won_procuremnt", digits=(3, 2))

    @api.one
    @api.depends('procurement_id')
    def _compute_price_won_procuremnt(self):
        self.price_won_procurement = 0
        for expertise_result_id in self.procurement_id.expertise_result_ids:
            if expertise_result_id.expertise_results == 1:
                self.price_won_procurement = expertise_result_id.exposure_price_with_vat
                break
