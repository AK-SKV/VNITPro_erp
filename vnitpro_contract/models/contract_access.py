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


class ContractAccess(models.Model):
    _name = 'vnitpro.contract.access'

    contract_id = fields.Many2one('vnitpro.contract', 'Contract', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', 'User', required=True, ondelete='cascade')
    access_date = fields.Datetime('Access date', required=True, default=lambda self: fields.datetime.now())


class Contract(models.Model):
    _inherit = 'vnitpro.contract'

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        if 'bin_size' in self._context:
            access = self.env['vnitpro.contract.access'].search(
                [('contract_id', '=', self.id), ('user_id', '=', self.env.user.id)], limit=1)
            if not access:
                self.env['vnitpro.contract.access'].create({'contract_id': self.id, 'user_id': self.env.user.id})
            else:
                access.write({'access_date': datetime.datetime.now()})
        return super(Contract, self).read(fields, load)


class AccessContract(models.Model):
    _name = 'vnitpro.contract.access.recent'
    _order = 'access_date desc'
    _auto = False

    access_date = fields.Datetime("Access date", required=False, )
    code = fields.Char('Code', size=50, required=True, track_visibility="onchange")
    name = fields.Char('Name', size=255, required=True, track_visibility="onchange")
    user_id = fields.Many2one('res.users', 'User', required=True, ondelete='cascade')

    def detail_contract(self):
        access = self.env['vnitpro.contract.access'].search(
            [('contract_id', '=', self.id), ('user_id', '=', self.env.user.id)], limit=1)
        if not access:
            self.env['vnitpro.contract.access'].create({'contract_id': self.id, 'user_id': self.env.user.id})
        else:
            access.write({'access_date': datetime.datetime.now()})

        view_id = self.env['ir.ui.view'].search(
            [('name', '=', 'vnitpro.contract.form'), ('model', '=', 'vnitpro.contract')], limit=1).id
        return {
            'name': 'Contract',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'res_model': 'vnitpro.contract',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id or False,
        }

    @api.model_cr
    def init(self):
        self._cr.execute("""
            DROP VIEW IF EXISTS vnitpro_contract_access_recent;
            CREATE VIEW vnitpro_contract_access_recent as
              (
                SELECT
                    ac.id access_id,
                    ac.access_date,
                    ac.user_id,
                    ct.*
                FROM vnitpro_contract_access ac
                LEFT JOIN vnitpro_contract ct
                    ON ac.contract_id = ct.id
              );
        """)
