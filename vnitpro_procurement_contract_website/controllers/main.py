# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import logging
import werkzeug
_logger = logging.getLogger(__name__)


class Website(Home):

    @http.route('/', type='http', auth="user", website=True)
    def index(self, **kw):
        return werkzeug.utils.redirect('/web')
