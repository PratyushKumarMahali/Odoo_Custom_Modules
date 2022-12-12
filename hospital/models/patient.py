from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _order = "patient_inscription_id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_patient_progress(self):
        return "Condition Pre-Evaluation"
    
    def _get_default_id(self):
        return 1
    
    name = fields.Char(string="Search")
    
    patient_inscription_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    patient_image = fields.Binary(string="Image", attachment=True, track_visibility="always")
    patient_name = fields.Char(string="Name", required=True, track_visibility="always")
    patient_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', required=True, store=True, track_visibility="always")
    patient_birth_date = fields.Date(string="Birth Date", required=True, track_visibility="always")
    patient_age = fields.Integer(string="Age", compute="_patient_age", readonly=True, store=True, track_visibility="always", group_operator=False)
    patient_age_group = fields.Selection([('major', 'Major'), ('minor', 'Minor')], string='Age Group', compute="_patient_age_group", readonly=True, store=True, track_visibility="always")
    patient_email = fields.Char(string="Email", default='text@mail.com', track_visibility="always")
    patient_contact = fields.Integer(string="Contact", track_visibility="always")
    patient_progress = fields.Text(string="Progress", default=_get_default_patient_progress, track_visibility="always")
    
    appointment_count = fields.Integer(string="Appointments", compute="get_appointment_count")
    
    active = fields.Boolean(string="Active", default=True)
    
    doctor_inscription_id = fields.Many2one('hospital.doctor', string="Doctor", default=_get_default_id, required=True, track_visibility="always")
    doctor_gender = fields.Selection(string='Doctor Gender', related='doctor_inscription_id.doctor_gender', readonly=True, store=True)
    user_id = fields.Many2one('res.users', related='doctor_inscription_id.user_id', string='Doctor Related User')
    
    @api.model
    def create(self, vals):
        if vals.get('patient_inscription_id', _('New')) == _('New'):
            vals['patient_inscription_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
    
    @api.depends('patient_birth_date')
    def _patient_age(self):
        today = date.today()
        for record in self:
            if record['patient_birth_date']:
                record['patient_age'] = today.year - record['patient_birth_date'].year - ((today.month, today.day) < (record['patient_birth_date'].month, record['patient_birth_date'].day))
            else:
                record['patient_age'] = False
                
    @api.depends('patient_age')
    def _patient_age_group(self):
        for record in self:
            if record.patient_age:
                if record.patient_age < 18:
                    record.patient_age_group = 'minor'
                else:
                    record.patient_age_group = 'major'
                    
    @api.constrains('patient_age')
    def _patient_age_constrains(self):
        for record in self:
            if record.patient_age <= 5:
                raise ValidationError(_('Patient with Age 5 or Below is not Diagnosed!!!'))
    
    @api.constrains('patient_contact')
    def _patient_contact_constrains(self):
        for record in self:
            if len(str(record.patient_contact)) != 7:
                raise ValidationError(_('Patient Contact should be 7 Digits!!!'))
    
    @api.multi
    def patient_appointments(self):
        return{
            'name': _('Appointments'),
            'domain': [('patient_inscription_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_inscription_id', '=', self.id)])
        self.appointment_count = count
        
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.patient_inscription_id, record.patient_name)))
        return result
    
    def action_send_card(self):
        for record in self:
            template_id = record.env.ref('hospital.patient_card_email_template').id
            template = record.env['mail.template'].browse(template_id)
            template.send_mail(record.id, force_send=True)
