from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalDoctor(models.Model):
    
    _name = 'hospital.doctor'
    _description = 'Doctor Record'
    _rec_name = 'doctor_name'
    _order = "doctor_inscription_id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_id(self):
        return 1
    
    name = fields.Char(string="Search")
    
    doctor_inscription_id = fields.Char(string='Doctor ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    doctor_image = fields.Binary(string="Image", attachment=True, track_visibility="always")
    doctor_name = fields.Char(string="Name", required=True, track_visibility="always")
    doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', required=True, store=True, track_visibility="always")
    doctor_birth_date = fields.Date(string="Birth Date", required=True, track_visibility="always")
    doctor_age = fields.Integer(string="Age", compute="_doctor_age", readonly=True, store=True, track_visibility="always", group_operator=False)
    doctor_email = fields.Char(string="Email", default='text@mail.com', track_visibility="always")
    doctor_contact = fields.Integer(string="Contact", track_visibility="always")
    
    user_id = fields.Many2one('res.users', default=_get_default_id, string='Related User', readonly=True, track_visibility="always")
    
    patient_count = fields.Integer(string="Patients", compute="get_patient_count")
    
    active = fields.Boolean(string="Active", default=True)
    
    doctor_name_upper = fields.Char(string="Name UPPER", compute="compute_upper_name", inverse="inverse_upper_name", track_visibility="always")
    doctor_name_lower = fields.Char(string="Name lower", compute="compute_lower_name", track_visibility="always")
    
    @api.depends('doctor_name')
    def compute_upper_name(self):
        for record in self:
            record.doctor_name_upper = record.doctor_name.upper() if record.doctor_name else False
            
    def inverse_upper_name(self):
        for record in self:
            record.doctor_name = record.doctor_name_upper.lower() if record.doctor_name_upper else False        
            
    @api.depends('doctor_name')
    def compute_lower_name(self):
        for record in self:
            record.doctor_name_lower = record.doctor_name.lower() if record.doctor_name else False
            
    @api.model
    def create(self, vals):
        if vals.get('doctor_inscription_id', _('New')) == _('New'):
            vals['doctor_inscription_id'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')
        result = super(HospitalDoctor, self).create(vals)
        return result
    
    @api.depends('doctor_birth_date')
    def _doctor_age(self):
        today = date.today()
        for record in self:
            if record['doctor_birth_date']:
                record['doctor_age'] = today.year - record['doctor_birth_date'].year - ((today.month, today.day) < (record['doctor_birth_date'].month, record['doctor_birth_date'].day))
            else:
                record['doctor_age'] = False
                
    @api.constrains('doctor_age')
    def _doctor_age_constrains(self):
        for record in self:
            if record.doctor_age <= 21:
                raise ValidationError(_('Doctor with Age 21 or Below is not Employed!!!'))
    
    @api.constrains('doctor_contact')
    def _doctor_contact_constrains(self):
        for record in self:
            if len(str(record.doctor_contact)) != 7:
                raise ValidationError(_('Doctor Contact should be 7 Digits!!!'))
            
    @api.multi
    def doctor_patients(self):
        return{
            'name': _('Patients'),
            'domain': [('doctor_inscription_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    def get_patient_count(self):
        count = self.env['hospital.patient'].search_count([('doctor_inscription_id', '=', self.id)])
        self.patient_count = count
        
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.doctor_inscription_id, record.doctor_name)))
        return result
