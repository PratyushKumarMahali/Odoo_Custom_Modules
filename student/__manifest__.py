{
    'name': "Student Management",
    'summary': "Student Management",
    'description': "Module for Managing Students",
    'author': "PkM",
    'maintainer': "PkM",
    'website': "http://www.pkm.com",
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.0',
    'sequence': 1,
    'license': 'LGPL-3',
    # Other module necessary for this one to work correctly
    'depends': ['base', 'mail'],
    # Loads with this model
    'data': [
        'security/security.xml',
        # 'security/rule.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'wizard/student_wizard.xml',
        'views/sequence_student.xml',
        'views/student_view.xml',
        'views/school_view.xml',
        'views/res_partner_inherit.xml',
        'views/cron.xml',
        ],
    # Loads when demo data is selected
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}