# -*- coding:utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.modules import get_module_path
import os
import logging
_logger = logging.getLogger(__name__)


class base_language_update(models.TransientModel):
    _name = "base.language.update"

    def update_language(self):
        context = dict(self._context)
        context['overwrite'] = True
        path_module = get_module_path('vietnam_translate')
        print(path_module)
        if path_module:
            path_module += '/i18n'
            files = os.listdir(path_module)
            if files:
                for f in files:
                    module_name = f.split('.')[0]
                    modules = self.env['ir.module.module'].sudo().search(
                        [('name', '=', module_name)])
                    if modules:
                        tools.trans_load(self._cr, path_module + '/' + f, 'vi_VN',
                                         verbose=False, module_name=modules[0].name, context=context)
        return {'type': 'ir.actions.act_window_close'}
