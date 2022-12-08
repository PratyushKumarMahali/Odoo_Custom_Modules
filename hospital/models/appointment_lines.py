from odoo import models, fields, api


class HospitalAppointmentLines(models.Model):
    
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines Record'
    
    appointment_inscription_id = fields.Many2one("hospital.appointment", string="Appointment ID")
    
    product_id = fields.Many2one("product.product", string="Medicine")
    product_qty = fields.Float(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price", related='product_id.lst_price', readonly=True)
    price_subtotal = fields.Float(string="Sub-total", compute="sub_total", readonly=True)
    
    @api.depends('price_unit', 'product_qty')
    def sub_total(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_qty
