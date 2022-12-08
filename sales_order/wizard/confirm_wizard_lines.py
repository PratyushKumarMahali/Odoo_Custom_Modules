from odoo import fields, models, api


class ConfirmWizardLines(models.TransientModel):
    _name = "confirm.wizard.lines"
    _description = "Confirm Wizard Lines"
    
    product_id = fields.Many2one("product.product", string="Product", required=True)
    description = fields.Text(string="Description", readonly=True)
    product_uom_qty = fields.Float(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price", readonly=True)
    price_subtotal = fields.Float(string="Sub-total", compute="sub_total", readonly=True)
    
    orders_id = fields.Many2one('confirm.wizard', string="Orders ID")
    
    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price
            self.description = self.product_id.name
            
    @api.depends('price_unit', 'product_uom_qty')
    def sub_total(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_uom_qty
