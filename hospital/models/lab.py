from odoo import models, fields, api, _


class HospitalLab(models.Model):
    _name = 'hospital.lab'
    _description = 'Hospital Laboratory'
    _rec_name = 'lab_inscription_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_id(self):
        return 1
    
    def _get_default_lab_result(self):
        return "Test Evaluation"

    lab_inscription_id = fields.Char(string='Laboratory ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    appointment_inscription_id = fields.Many2one('hospital.appointment', string="Appointment", default=_get_default_id, required=True, track_visibility="always")
    patient_inscription_id = fields.Many2one('hospital.patient', string="Patient", related='appointment_inscription_id.patient_inscription_id', readonly=True, track_visibility="always")
    doctor_inscription_id = fields.Many2one('hospital.doctor', string="Doctor", related='patient_inscription_id.doctor_inscription_id', readonly=True, track_visibility="always")
    user_id = fields.Many2one('res.users', related='doctor_inscription_id.user_id', string='Doctor Related User', readonly=True, track_visibility="always")
    
    lab_result = fields.Text(string='Laboratory Results', default=_get_default_lab_result, track_visibility="always")
    
    @api.model
    def create(self, vals):
        if vals.get('lab_inscription_id', _('New')) == _('New'):
            vals['lab_inscription_id'] = self.env['ir.sequence'].next_by_code('hospital.lab.sequence') or _('New')
        result = super(HospitalLab, self).create(vals)
        return result
