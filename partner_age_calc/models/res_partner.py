from odoo import models, fields, api
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", compute="partner_age")
    
    @api.depends('birth_date')
    def partner_age(self):
        today = date.today()
        for record in self:
            if record['birth_date']:
                record['age'] = today.year - record['birth_date'].year - ((today.month, today.day) < (record['birth_date'].month, record['birth_date'].day))
            else:
                record['age'] = False
                
    @api.model
    def birth_date_email(self):
        print("** Cron Start **")
        customer = self.env['res.partner'].search([])
        template_id = self.env.ref('partner_age_calc.birth_date_email_template')
        today = date.today()
        for record in customer:
            if record.birth_date:
                if ((record['birth_date'].month, record['birth_date'].day) == (today.month, today.day)):
                    template_id.send_mail(record.id, force_send=True, raise_exception=True)
                    print("** Birthday Found **")