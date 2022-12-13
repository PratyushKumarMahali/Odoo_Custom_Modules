from odoo import models, fields, api, _
from datetime import date


class HospitalAppointment(models.Model):
    
    _name = 'hospital.appointment'
    _description = 'Appointment Record'
    _rec_name = 'appointment_inscription_id'
    _order = "appointment_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_appointment_progress(self):
        return "Condition Post-Evaluation"
    
    def _get_default_id(self):
        return 1
    
    name = fields.Char(string="Search")
    
    appointment_inscription_id = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    patient_inscription_id = fields.Many2one('hospital.patient', string="Patient", default=_get_default_id, required=True, track_visibility="always")
    patient_gender = fields.Selection(string='Patient Gender', related='patient_inscription_id.patient_gender', readonly=True, store=True)
    patient_age = fields.Integer(string="Patient Age", related='patient_inscription_id.patient_age', readonly=True)
    patient_email = fields.Char(string="Patient Email", related='patient_inscription_id.patient_email', readonly=True)
    patient_contact = fields.Integer(string="Patient Contact", related='patient_inscription_id.patient_contact', readonly=True)
    patient_progress = fields.Text(string="Information", related='patient_inscription_id.patient_progress', readonly=True)
    doctor_inscription_id = fields.Many2one('hospital.doctor', string="Doctor", related='patient_inscription_id.doctor_inscription_id', readonly=True, track_visibility="always")
    doctor_gender = fields.Selection(string='Doctor Gender', related='patient_inscription_id.doctor_gender', readonly=True, store=True)
    appointment_progress = fields.Text(string="Progress", default=_get_default_appointment_progress, track_visibility="always")
    appointment_date = fields.Date(string="Appointment Date", required=True, track_visibility="always")
    
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string='Status', readonly=True, default='draft', track_visibility='onchange')
    
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_inscription_id', string="Appointment Lines", track_visibility="always")
    
    pharmacy = fields.Char(string="Pharmacy")
    
    @api.model
    def create(self, vals):
        if vals.get('appointment_inscription_id', _('New')) == _('New'):
            vals['appointment_inscription_id'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    
    def action_confirm(self):
        for record in self:
            record.state = 'confirm'
    
    def action_done(self):
        for record in self:
            record.state = 'done'
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
            
    def action_draft(self):
        for record in self:
            record.state = 'draft'
            
    @api.model
    def appointment_cron(self):
        appointment = self.env['hospital.appointment'].search([])
        template_id = self.env.ref('hospital.patient_card_email_template')
        today = date.today()
        for record in appointment:
            if record.appointment_date:
                if ((record['appointment_date'].year, record['appointment_date'].month, record['appointment_date'].day) == (today.year, today.month, today.day)):
                    template_id.send_mail(record.patient_inscription_id.id, force_send=True)
