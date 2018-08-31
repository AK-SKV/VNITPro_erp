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

    processing_situation_ids = fields.One2many('vnitpro.processing.situation', 'procurement_id', 'Processing Situation')


class ProcessingSituation(models.Model):
    _name = "vnitpro.processing.situation"

    procurement_id = fields.Many2one('vnitpro.procurement', 'Procurement', ondelete="cascade")
    # Content Delivered
    deliver_proponent = fields.Char('Deliver/ Proponent', size=200, required=True)
    kind_of_work = fields.Char('Kind Of Work', size=200, required=True)
    content_delivered = fields.Char('Content Delivered', size=200, required=True)
    delivery_date = fields.Date('Deliver Date', size=200, required=True)

    # Perform Receive
    representative = fields.Char('Representative', size=200, required=True)
    content_situation = fields.Char('Content Situation', size=200, required=True)
    delivery_date_situation = fields.Date('Delivery Date Situation', size=200, required=True)
    receiver = fields.Char('Receiver', size=200, required=True)

    # Perform Situation
    content_implementation = fields.Char('Content Implementation', size=200, required=True)
    date_of_implementation = fields.Date('Date Of Implementation', size=200, required=True)

    attachment_ids = fields.One2many('vnitpro.base.attachment', 'processing_situation_id', 'Attach Files')


class BaseAttachment(models.Model):
    _inherit = "vnitpro.base.attachment"

    processing_situation_id = fields.Many2one('vnitpro.processing.situation', 'Processing Situation',
                                              ondelete="cascade")
