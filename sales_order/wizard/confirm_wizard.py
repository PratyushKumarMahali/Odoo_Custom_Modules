from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ConfirmWizard(models.TransientModel):
    _name = "confirm.wizard"
    _description = "Confirm Wizard"
    
    orders_lines = fields.One2many('confirm.wizard.lines', 'orders_id', string='Order Lines')
    
    @api.multi
    def add_product(self):
        active_ids = self.env['sale.order'].browse(self.env.context.get('active_ids'))
        for record in active_ids:
            if record.state == 'sale':
                raise ValidationError(_("One or More Orders Already Confirmed!!!"))
            for lines in self.orders_lines:
                results = {
                    'product_id': lines.product_id.id,
                    'product_uom_qty': lines.product_uom_qty,
                    'order_id': record.id
                    }
                self.env['sale.order.line'].create(results)

    # def confirm_order(self):
    #     active_ids = self.env['sale.order'].browse(self.env.context.get('active_ids'))
    #     for record in active_ids:
    #         if record.state == 'draft':
    #             record.action_confirm()
    #
    # def quote_order(self):
    #     active_ids = self.env['sale.order'].browse(self.env.context.get('active_ids'))
    #     for record in active_ids:
    #         if record.state == 'sale':
    #             record.action_cancel()
    #             record.action_draft()
