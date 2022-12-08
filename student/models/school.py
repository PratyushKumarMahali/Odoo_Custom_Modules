from odoo import models, fields


class School(models.Model):
    _name = 'school.school'
    _description = 'School Record'
    
    name = fields.Char(string="Name")
    student_ids = fields.One2many('student.student', 'school_id', string="Students")
