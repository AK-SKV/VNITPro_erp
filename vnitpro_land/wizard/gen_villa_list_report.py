# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)

LAND_TYPE = [
    ('1st_grade_house', '1st Grade House'),
    ('2nd_grade_house', '2nd Grade House'),
    ('3th_grade_house', '3th Grade House'),
    ('4th_grade_house', '4th Grade House'),
    ('apartment', 'Apartment'),
    ('villa', 'Villa'),
]


class GenerateVillaListReport(models.TransientModel):
    _name = 'vnitpro.gen.villa.list.report'

    name = fields.Char('Name', compute='compute_name')
    land_type = fields.Selection(LAND_TYPE, default="villa", readonly=True)
    land_group_id = fields.Many2one('vnitpro.land.group', 'Land Group', domain="[('activate','=','usage')]")
    ward_id = fields.Many2one('vnitpro.res.ward', 'Ward', domain=lambda self: self.get_domain())

    @api.multi
    @api.onchange('land_type')
    def change_land_type(self):
        for record in self:
            if record.land_group_id.land_type != record.land_type:
                record.land_group_id = False

    # def count_villa_ids(self):
    #     data = self.read(['land_type', 'land_group_id', 'ward_id'])[0]
    #     domains = []
    #     if self.land_type:
    #         domains += [('land_type', '=', self.land_type)]
    #     if self.land_group_id:
    #         domains += [('land_group_id', '=', self.land_group_id)]
    #     if self.ward_id:
    #         domains += [('ward_id', '=', self.ward_id)]
    #     villa_ids = self.env['vnitpro.land.use.rights'].search(domains, order="ward_id")
    #     data.update({'villa_ids': villa_ids.ids})
    #     _logger.warning(villa_ids)
    #     return data

    @api.multi
    def gen_villa_list_report_xlsx(self):
        return self.env.ref('vnitpro_land.act_gen_villa_list_report').report_action(self)

    @api.multi
    def gen_villa_list_report_pdf(self):
        data = self.read(['land_type', 'land_group_id', 'ward_id'])[0]
        domains = []
        if self.land_type:
            domains += [('land_type', '=', self.land_type)]
        if self.land_group_id:
            domains += [('land_group_id', '=', self.land_group_id)]
        if self.ward_id:
            domains += [('ward_id', '=', self.ward_id)]
        villa_ids = self.env['vnitpro.land.use.rights'].search(domains, order="ward_id")
        data.update({'villa_id': villa_ids.ids})
        _logger.warning(data)
        return self.env.ref('vnitpro_land.act_gen_villa_list_report_pdf').report_action(self, data=data)

    def get_domain(self):
        domain = []
        district = self.env.ref('vnitpro_base.vietnam_district_hai_ba_trung_hn', False)
        domain = [('district_id', '=', district.id)]
        return domain

    @api.one
    def compute_name(self):
        self.name = (_("Create Report"))
