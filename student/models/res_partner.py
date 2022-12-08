from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(string="Age")
    gstin = fields.Char(string="GST-IN")
    message = fields.Char(string="Message")

    @api.model
    def create(self, vals):
        print("** Override Contact Create Method **")
        if not vals['email']:
            raise ValidationError(_("Email required"))
        result = super(ResPartner, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        print("** Override Contact Write Method **")
        if vals.get('name') == 'test':
            vals['name'] = 'Blank'
        if vals.get('message') == 'test2':
            vals['message'] = 'Blank2'
        result = super(ResPartner, self).write(vals)
        return result

    @api.multi
    def unlink(self):
        print("** Override Contact Unlink Method **")
        for record in self:
            if record.age <= 20:
                raise ValidationError(_("Too Young to Unlink"))
        return super(ResPartner, self).unlink()
