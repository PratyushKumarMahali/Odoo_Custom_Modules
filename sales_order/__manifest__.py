{
    'name': "Sales Order",
    'summary': "Custom Button",
    'description': "Module for Custom Sales Order",
    'author': "PkM",
    'maintainer': "PkM",
    'website': "http://www.pkm.com",
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.0',
    'sequence': 3,
    'license': 'LGPL-3',
    # Other module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management'],
    # Loads with this model
    'data': [
        'security/ir.model.access.csv',
        'wizard/confirm_wizard.xml',
        ],
    # Loads when demo data is selected
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
