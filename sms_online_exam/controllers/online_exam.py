# -*- coding: utf-8 -*-
###############################################################################
#
#    Công ty giải pháp phần mềm VNITPro.
#    Copyright (C) 2018-TODAY VNITPro(<http://vnitpro.vn>).
#
###############################################################################

from datetime import datetime
from odoo import http, _
from odoo.http import request
import logging
import werkzeug
_logger = logging.getLogger(__name__)
import uuid


class OnlineExamController(http.Controller):

    @http.route('/online-exam', auth='user', type='http', website=True)
    def view_online_exam(self, **kw):
        exam_list = http.request.env['sms.online.exam'].sudo().search([('activate', '=', 'usage')])
        position_list = http.request.env['sms.online.exam.object'].sudo().search([('activate', '=', 'usage')])
        contestant_list = http.request.env['sms.online.exam.contestant'].sudo().search([('activate', '=', 'usage')])
        token = uuid.uuid4().__str__()
        return request.render('sms_online_exam.online_exam_register_page',
                              {'exam_list': exam_list, 'position_list': position_list, 'contestant_list': contestant_list, 'token': token})

    @http.route('/online-exam/check-exam', auth='user', type='http', website=True)
    def check_exam(self, **kw):
        if 'exam_list' in kw and 'identity_card' in kw:
            result_ids = http.request.env['sms.online.exam.result'].search(
                [('indentity_card', '=', kw['identity_card']), ('exam_id', '=', int(kw['exam_list']))], limit=1)
            if len(result_ids) > 0:
                return request.render('sms_online_exam.online_exam_done_page')
            else:
                token = kw['token'] if 'token' in kw else ''
                exam_id = http.request.env['sms.online.exam'].browse([int(kw['exam_list'])])
                return werkzeug.utils.redirect("/online-exam/" + exam_id.slug + "/" + token)
        else:
            return _('We have errors from system, please contact with Administrator or Developer for help ! Thank you.')

    @http.route('/online-exam/<exam_slug>/<string:token>', auth='user', type='http', website=True)
    def do_exam(self, exam_slug, token, **kw):
        _logger.warning(kw)
        return request.render('sms_online_exam.online_exam_contest_page')
