from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Record'
    
    student_inscription_id = fields.Char(string="Inscription ID")
    
    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    join_date = fields.Date(string="Join Date")
    
    address = fields.Char(string="Address")
    city = fields.Char(string="City")

    note_1 = fields.Float(string="Note 1")
    note_2 = fields.Float(string="Note 2")
    note_3 = fields.Float(string="Note 3")
    note_4 = fields.Float(string="Note 4")
    average = fields.Float(string="Average", compute="get_average_student")
    
    school_id = fields.Many2one('school.school', string="School")
    
    option_ids = fields.Many2many('student.option', string="Options")
    
    status = fields.Selection([('new', 'New'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new')
    
    greetings = fields.Char(string="Greetings", compute="welcome_student")
    
    message_onchange = fields.Char(string="Message")
    
    @api.depends('note_1', 'note_2', 'note_3', 'note_4')
    def get_average_student(self):
        self.average = (self.note_1 + self.note_2 + self.note_3 + self.note_4) / 4
        
    def set_student_to_accepted(self):
        template_id = self.env.ref('student.student_accept_email_template')
        self.status = 'accepted'
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True, email_values={"email_to":self.email})                

    def set_student_to_rejected(self):
        template_id = self.env.ref('student.student_reject_email_template')
        self.status = 'rejected'
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True, email_values={"email_to":self.email})
            
    @api.model
    def create(self, vals):
        print("** Override Student Create Method **")
        vals['student_inscription_id'] = self.env['ir.sequence'].next_by_code('student.sequence')
        result = super(Student, self).create(vals)
        return result
    
    @api.multi
    @api.depends('name')
    def welcome_student(self):
        for record in self:
            if record.name:
                record.greetings = 'Welcome ' + record.name + '. Fill every field with utmost care.'

    @api.onchange('name')
    def message(self):
        if self.name:
            self.message_onchange = 'Hello ' + self.name

    @api.constrains('age')
    def check_age(self):
        if self.age >= 30:
            raise ValidationError(_("Age Limit Under 30. Re-check & Submit!!!"))

    @api.constrains('name')
    def check_name(self):
        if self.name == 'test':
            raise ValidationError(_("Name Error. Re-check & Submit!!!"))
    
    @api.model
    def student_cron(self):
        print("** Student Cron **")
        students = self.env['student.student'].search([])
        for student in students:
            student.city = 'BBSR'
