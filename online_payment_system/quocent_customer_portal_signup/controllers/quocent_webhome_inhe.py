# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com
from odoo.addons.web.controllers.main import Home, ensure_db, SIGN_UP_REQUEST_PARAMS
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request
from datetime import datetime

class QcentWebHome(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                # failure_env = request.env['qcent.login.failure'].sudo()
                if request.session.__getattr__('login_attempts'):
                    val = request.session.__getattr__('login_attempts')
                    val += 1
                    request.session.__setattr__('login_attempts', val)
                    fail_session_id = request.session.__getattr__('fail_session_id')
                    # fail_session = failure_env.browse(fail_session_id)
                    # fail_session.write({
                    #     'attempt_count': val,
                    #     'attempt_time': datetime.now(),
                    # })
                else:
                    request.session.__setattr__('login_attempts', 1)
                    usr_id = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
                    # fail_session = failure_env.create({
                    #     'ip': request.httprequest.remote_addr,
                    #     'usr_id': usr_id.id if usr_id else False,
                    #     'attempt_count': 1, 'attempt_time': datetime.now(),
                    # })
                    # request.session.__setattr__('fail_session_id', fail_session.id)

                if request.session.login_attempts >= 3:
                    fail_msg = f"""You have {request.session.login_attempts} failed login attempts.
                                Kindly try to reset your password using the Reset Password link below."""
                else:
                    fail_msg = f"You have {request.session.login_attempts} failed login attempts."

                values['fail_msg'] = fail_msg
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')
        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')
        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True
        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        response.qcontext.update(self.get_auth_signup_config())
        return response
    
    # New Implementation
    # Pass 'login_captcha' value to the server
    @http.route('/login_captcha_value', type='json', auth='public', methods=['POST'], website=True)
    def login_captcha_value(self, **kwargs):
        return request.env['res.config.settings'].get_values().get('login_captcha')
