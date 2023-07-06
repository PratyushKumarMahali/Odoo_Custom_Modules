# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com

from odoo import http
from odoo.addons.web.controllers import main
from odoo.http import request
from odoo.exceptions import AccessDenied


class QcentWebHome(main.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        if not request.uid:
            request.uid = request.env.ref('base.public_user').id
        if request.httprequest.method == 'POST':
            param = request.env['ir.config_parameter'].sudo()
            enable_email_otp_login = param.get_param('quocent_customer_portal_signup.enable_email_otp_login')
            if not enable_email_otp_login:
                return super(QcentWebHome, self).web_login(redirect)
            try:
                uid = request.env['res.users'].sudo().search(['|', ('login', '=', request.params['login']), ('cust_code', '=', request.params['login'])])
                if uid:
                    if uid.id != 2:
                        user = uid.with_user(uid)
                        login, passwd = request.params['login'], request.params['password']
                        vals = dict(uid=uid.id, db=request.session.db, login=login, passwd=passwd)
                        uid.sudo().generate_otp_in_db()
                        return request.render("qcent_login_otp_email.verify_otp_template", vals)
                    else:
                        return super(QcentWebHome, self).web_login(redirect)
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except AccessDenied as e:
                pass
        return super(QcentWebHome, self).web_login(redirect)

    @http.route('/web/verify/otp', type='http', auth="none", csrf=False, website=True)
    def web_verify_otp(self, **kw):
        entered_otp, uid = request.params.get('otp'), request.params.get('uid')
        res = request.env['res.users'].browse(int(uid)).sudo().verify_otp(entered_otp)
        login, passwd = request.params['login'], request.params['passwd']
        vals = dict(uid=uid, db=request.session.db, login=login, passwd=passwd,
                    wrong_login=False, otp_expire=False)
        if res == 1:
            try:
                uid = request.session.authenticate(request.session.db,
                                                   request.params['login'],
                                                   request.params['passwd'])
            except AccessDenied as e:
                vals.update(wrong_login=True)
                return request.render("qcent_login_otp_email.verify_otp_template", vals)
            redirect = request.params['redirect']
            return request.redirect(self._login_redirect(uid, redirect=redirect))
        elif res == -1:
            vals.update(otp_expire=True)
            return request.render("qcent_login_otp_email.verify_otp_template", vals)
        vals.update(wrong_otp=True)
        return request.render("qcent_login_otp_email.verify_otp_template", vals)
