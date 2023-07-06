# -*- coding: utf-8 -*-
# Quocent Pvt. Ltd.
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
# https://www.quocent.com
{
    'name': 'Quocent - Customer portal signup',
    'author': 'Quocent Pvt. Ltd.',
    'summary': 'Signup Enhancement',
    'website': 'https://www.quocent.com',
    'license': 'LGPL-3',
    'description': """
    This is a customization to odoo’s portal sign up process. By default when a user signs up on
Odoo portal using the Signup form, a new res.partner record is created and its portal user is
created.
However, in this case, the res.partner record is already available in the system. The
Sign Up form will be used to validate the customer with the existing customer database and
create a portal user on successful sign up.
    """,
    'depends': ['base','auth_signup', 'auth_password_policy_signup', 'web', 'google_recaptcha'],
    'data': [
        'views/res_partner_inhe.xml',
        'views/res_config_inhe.xml',
        'views/signup_tmpl_inhe.xml',
        'views/wc_login_tmpl.xml',
        'views/web_website_inhe.xml',
     ],
    'assets': {
            'web.assets_frontend': [
                'quocent_customer_portal_signup/static/src/js/password_length.js',
                'quocent_customer_portal_signup/static/src/js/form_validations.js',
                'quocent_customer_portal_signup/static/src/js/login_captcha.js',
            ],
        },
    'installable': True,
    'auto_install': False,
}