# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com

{
    'name': 'Quocent - Users email OTP login',
    'author': 'Quocent Pvt. Ltd.',
    'summary': '',
    'description': '',
    'depends': ['base', 'web', 'website', 'mail', 'quocent_customer_portal_signup'],
    'data': [
        'data/email_otp_template.xml',
        'views/web_tmpl_enter_otp.xml',
     ],
    'installable': True,
    'auto_install': False,
}
