from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    birthdate = fields.Date(string='Birth Date')
    
    @api.onchange('partner_id')
    def birth_date_sale_order(self):
        if self.partner_id:
                self.birthdate = self.partner_id.birth_date
