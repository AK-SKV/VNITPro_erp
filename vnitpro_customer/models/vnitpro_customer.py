# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, fields, api, _


class Customer(models.Model):
    _name = "vnitpro.customer"
    _inherit = "vnitpro.base.person"

    language = fields.Many2one('res.lang', 'Language', default=75)
    website = fields.Char('Website')
    customer_type = fields.Selection([('individual', 'Individual'),
                                      ('company', 'Company')], 'Customer Type', default='individual')
    job_position = fields.Char('Job Position')
    company_id = fields.Many2one('vnitpro.customer', 'Company', domain="[('customer_type','=','individual')]",
                                 ondelete='cascade')
    parent_id = fields.Many2one('vnitpro.customer', 'Parent', ondelete='cascade')
    child_ids = fields.One2many('vnitpro.customer', 'parent_id', 'Child')
