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

JOBTYPE = []


class Project(models.Model):
    _inherit = 'vnitpro.project'

    project_processing_ids = fields.One2many('vnitpro.project.processing', 'project_id', string="Project Processing")


class ProjectProcessing(models.Model):
    _name = "vnitpro.project.processing"

    project_id = fields.Many2one('vnitpro.project', 'Project', required=True, ondelete="cascade")
    assignist = fields.Many2one('res.users', 'Assignist')
    job_type = fields.Selection(JOBTYPE, 'Job Type', required=True)
    processing_content = fields.Text('Processing Content', size=1000, required=True)
    time_assgin = fields.Datetime('Time Assgin')
    content_implementation = fields.Text('Content Impolementation', size=1000, required=True)
