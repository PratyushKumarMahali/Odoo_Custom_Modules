# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com

from odoo import models, fields, api


class QuocentSettingModification(models.TransientModel):
    _inherit = 'res.config.settings'
    
    login_captcha = fields.Boolean('Login Captcha')
    signup_captcha = fields.Boolean('Signup Captcha')
    extend_pdd = fields.Integer('Extend Payment Due Date By')
    recipient_email_ids = fields.Char('Recipient Email IDs')
    enable_email_otp_login = fields.Boolean("Email One Time Password (OTP)")
    email_otp_expire_duration = fields.Integer("Email OTP Expiration Duration")
    
    @api.model
    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()
        login_captcha = self.login_captcha or False
        signup_captcha = self.signup_captcha or False
        extend_pdd = self.extend_pdd or False
        recipient_email_ids = self.recipient_email_ids or False
        enable_email_otp_login = self.enable_email_otp_login or False
        email_otp_expire_duration = self.email_otp_expire_duration or False
        param.set_param('quocent_customer_portal_signup.login_captcha', login_captcha)
        param.set_param('quocent_customer_portal_signup.signup_captcha', signup_captcha)
        param.set_param('quocent_customer_portal_signup.extend_pdd', extend_pdd)
        param.set_param('quocent_customer_portal_signup.recipient_email_ids', recipient_email_ids)
        param.set_param('quocent_customer_portal_signup.enable_email_otp_login', enable_email_otp_login)
        param.set_param('quocent_customer_portal_signup.email_otp_expire_duration', email_otp_expire_duration)
        
    @api.model   
    def get_values(self):
        res = super().get_values()
        param = self.env['ir.config_parameter'].sudo()
        res.update(
            login_captcha=param.get_param('quocent_customer_portal_signup.login_captcha'),
            signup_captcha=param.get_param('quocent_customer_portal_signup.signup_captcha'),
            extend_pdd=param.get_param('quocent_customer_portal_signup.extend_pdd'),
            recipient_email_ids=param.get_param('quocent_customer_portal_signup.recipient_email_ids'),
            enable_email_otp_login=param.get_param('quocent_customer_portal_signup.enable_email_otp_login'),
            email_otp_expire_duration=param.get_param('quocent_customer_portal_signup.email_otp_expire_duration'),
        )
        return res
