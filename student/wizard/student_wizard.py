from odoo import models, fields


class StudentWizard(models.TransientModel):
    _name = 'student.wizard'
    _description = 'Student Wizard'
    
    address = fields.Char(string="Address")
    city = fields.Char(string="City")

    def update_student_information(self):
        print("** Update Student Information **")
        print("context", self.env.context)
        print("active_id", self.env.context.get("active_id"))
        print("city", self.city)
        print("address", self.address)
        self.env['student.student'].browse(self.env.context.get("active_id")).write({
            'city':self.city,
            'address':self.address
            })
        return {'type':'ir.actions.act_window_close'}