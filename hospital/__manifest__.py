{
    'name': "Hospital Management",
    'summary': "Hospital Management",
    'description': "Module for Managing Hospitals",
    'author': "PkM",
    'maintainer': "PkM",
    'website': "http://www.pkm.com",
    'category': 'Extra Tools',
    'version': '12.0.1.0.0',
    'sequence': 1,
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'sale', 'sale_management', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'security/rule.xml',
        'reports/patient_card_pdf.xml',
        'reports/report.xml',
        'data/sequence_patient.xml',
        'data/sequence_appointment.xml',
        'data/sequence_doctor.xml',
        'data/sequence_lab.xml',
        'data/mail_template.xml',
        'data/data.xml',
        'data/cron.xml',
        'wizards/create_appointment.xml',
        'views/appointment.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/hospital_menu.xml',
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
