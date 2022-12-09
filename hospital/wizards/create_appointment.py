from odoo import models, fields


class CreateAppointment(models.TransientModel):
    
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'
    
    patient_inscription_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")
    
    def create_appointment(self):
        vals = {
            'patient_inscription_id':self.patient_inscription_id.id,
            'appointment_date':self.appointment_date,
            'appointment_progress':'Created from Wizard'
            }
        self.env['hospital.appointment'].create(vals)
        return {'type':'ir.actions.act_window_close'}
