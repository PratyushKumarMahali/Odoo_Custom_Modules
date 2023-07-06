# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com
from odoo import fields, models, api


class ResPartnerInhe(models.Model):
    _inherit = 'res.partner'

    pan = fields.Char('PAN')


class ResUsersInhe(models.Model):
    _inherit = 'res.users'

    cust_code = fields.Char('Cust Code')

    @api.model
    def _get_login_domain(self, login):
        return ['|',('cust_code', '=', login),('login', '=', login)]

