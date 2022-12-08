{
    'name': "Partner Age Calculator",
    'summary': "Partner Age Calculator",
    'description': "Module for Calculating Age of Partner",
    'author': "PkM",
    'maintainer': "PkM",
    'website': "http://www.pkm.com",
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.0',
    'sequence': 2,
    'license': 'LGPL-3',
    # Other module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale_management'],
    # Loads with this model
    'data': [
        'data/email_template.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/cron.xml',
        ],
    # Loads when demo data is selected
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
