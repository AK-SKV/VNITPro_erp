# -*- coding: utf-8 -*-
###############################################################################
#
#    VNITPro Solutions Pvt. Ltd.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).

###############################################################################

from odoo import models, fields, api
import datetime
import logging

_logger = logging.getLogger(__name__)


class ProcurementAccess(models.Model):
    _name = 'vnitpro.procurement.access'

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', 'User', required=True, ondelete='cascade')
    access_date = fields.Datetime('Access date', required=True, default=lambda self: fields.datetime.now())


class Procurement(models.Model):
    _inherit = 'vnitpro.procurement'

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        if 'bin_size' in self._context:
            access = self.env['vnitpro.procurement.access'].search(
                [('procurement_id', '=', self.id), ('user_id', '=', self.env.user.id)], limit=1)
            if not access:
                self.env['vnitpro.procurement.access'].create({'procurement_id': self.id, 'user_id': self.env.user.id})
            else:
                access.write({'access_date': datetime.datetime.now()})
        return super(Procurement, self).read(fields, load)


class AccessProcurement(models.Model):
    _name = 'vnitpro.procurement.access.recent'
    _order = 'access_date desc'
    _auto = False

    access_date = fields.Datetime("Access date", required=False, )
    code = fields.Char('Code', size=50, required=True, track_visibility="onchange")
    name = fields.Char('Name', size=255, required=True, track_visibility="onchange")
    user_id = fields.Many2one('res.users', 'User', required=True, ondelete='cascade')

    def detail_procurement(self):
        access = self.env['vnitpro.procurement.access'].search(
            [('procurement_id', '=', self.id), ('user_id', '=', self.env.user.id)], limit=1)
        if not access:
            self.env['vnitpro.procurement.access'].create({'procurement_id': self.id, 'user_id': self.env.user.id})
        else:
            access.write({'access_date': datetime.datetime.now()})

        view_id = self.env['ir.ui.view'].search(
            [('name', '=', 'vnitpro.procurement.form'), ('model', '=', 'vnitpro.procurement')], limit=1).id
        return {
            'name': 'Procurement',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'res_model': 'vnitpro.procurement',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id or False,
        }

    @api.model_cr
    def init(self):
        self._cr.execute("""
            DROP VIEW IF EXISTS vnitpro_procurement_access_recent;
            CREATE VIEW vnitpro_procurement_access_recent as
              (
                SELECT
                    ac.id access_id,
                    ac.access_date,
                    ac.user_id,
                    gt.*
                FROM vnitpro_procurement_access ac
                LEFT JOIN vnitpro_procurement gt
                    ON ac.procurement_id = gt.id
              );
        """)
