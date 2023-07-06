# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http, tools, _
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.web.controllers.main import SIGN_UP_REQUEST_PARAMS
from . import quocent_exception
from odoo.addons.auth_signup.models.res_users import SignupError

import logging
import werkzeug
_logger = logging.getLogger(__name__)


class QcentSignUp(AuthSignupHome):

    @http.route('/get/partner/name', type='json', auth='public')
    def get_partner_name(self, code):
        if code:
            record = request.env['res.partner'].sudo().search([('ref', '=', code)])
            if record:
                return dict(name=record.name, email=record.email, pan=record.pan,
                            gst=record.vat, phone=record.mobile)
            return 'error'
        return 'error'

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (quocent_exception.DetailsNotFoundError, AssertionError) as e:
                _logger.error("%s", e)
                qcontext['error'] = _('''The system did not find any
                    related records for the combination of Email, Phone Number, PAN, Customer Code and GST provided.
                    Please provide correct details''')
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    # New Implementation
    # Pass 'signup_captcha' value to the server
    @http.route('/signup_captcha_value', type='json', auth='public', methods=['POST'], website=True)
    def signup_captcha_value(self, **kwargs):
        return request.env['res.config.settings'].get_values().get('signup_captcha')
    
    def get_auth_signup_config(self):
        d = super(QcentSignUp, self).get_auth_signup_config()
        d['password_minimum_length'] = request.env['ir.config_parameter'].sudo().get_param('auth_password_policy.minlength')
        return d

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering context for signup and reset password """
        SIGN_UP_REQUEST_PARAMS.update(('cust_code', 'pan_num', 'gst_num', 'phone_num'))
        qcontext = {k: v for (k, v) in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        qcontext.update(self.get_auth_signup_config())
        if not qcontext.get('token') and request.session.get('auth_signup_token'):
            qcontext['token'] = request.session.get('auth_signup_token')
        if qcontext.get('token'):
            try:
                token_infos = request.env['res.partner'].sudo().signup_retrieve_info(qcontext.get('token'))
                for k, v in token_infos.items():
                    qcontext.setdefault(k, v)
            except:
                qcontext['error'] = _("Invalid signup token")
                qcontext['invalid_token'] = True
        return qcontext

    def _prepare_signup_values(self, qcontext):
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'cust_code',
                                                     'pan_num', 'gst_num', 'phone_num')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values

    def _signup_with_values(self, token, values):
        domain = [('ref', '=', values.get('cust_code')), ('vat', '=', values.get('gst_num')),
                  ('pan', '=', values.get('pan_num')), ('phone', '=', values.get('phone_num')),
                  ('email', '=', values.get('login'))]
        partner = request.env['res.partner'].sudo().search(domain, limit=1)
        if not partner:
            raise quocent_exception.DetailsNotFoundError(_('''The system did not find any
                    related records for the combination of Email, Phone Number, PAN, Customer Code and GST provided.
                    Please provide correct details'''))

        del values['gst_num'], values['pan_num'], values['phone_num']
        values['partner_id'] = partner.id
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()
        uid = request.session.authenticate(db, login, password)
        if not uid:
            raise SignupError(_('Authentication Failed.'))