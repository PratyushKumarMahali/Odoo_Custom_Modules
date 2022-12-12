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
        self.patient_inscription_id.message_post(body="Appointment Created Successfully!!!", subject="Appointment Creation")
        self.env['hospital.appointment'].create(vals)
        return {'type':'ir.actions.act_window_close'}
    
    def get_data(self):
        if not self.patient_inscription_id:
            appointments = self.env['hospital.appointment'].search([])
        else:
            appointments = self.env['hospital.appointment'].search([('patient_inscription_id', '=', self.patient_inscription_id.id)])
        for record in appointments:
            print("Appointment ID", record.appointment_inscription_id)
