from odoo import models, fields


class StudentOption(models.Model):
    _name = 'student.option'
    _description = 'Student Activity Record'
    
    name = fields.Char(string="Name")
