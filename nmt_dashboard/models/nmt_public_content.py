from odoo import models, fields


class PublicContent(models.Model):
    
    _name = 'nmt.public.content'
    _description = 'Public Content'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'campaign'
    
    campaign_id = fields.Many2one('nmt.campaign', string="Campaign")
    client_id = fields.Many2one('res.partner', string="Client", required=True)
    responsible_id = fields.Many2one('res.users', string="Responsible")
    
    title = fields.Char(string="Title", required=True, size=28, tracking=True)
    subtitle = fields.Char(string="Subtitle", size=37, tracking=True)
    banner_id = fields.Many2one('ir.attachment', string="Banner", attachment=True, tracking=True)
    about_us = fields.Text(string="About Us", tracking=True)
    team_image_id = fields.Many2one('ir.attachment', string="Team Image", attachment=True, tracking=True)
    team_description = fields.Text(string="Team Description", tracking=True)
    pitch = fields.Text(string="Pitch", tracking=True)
    kanban_background_image_id = fields.Many2one('ir.attachment', string="Kanban Background Image", attachment=True, tracking=True)
    # image = fields.Binary(string="Image", attachment=True, tracking=True)
    
    def preview(self):
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Preview Click Successful',
                'type':'rainbow_man',
                }
            }
    
    def action_button_space(self):
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Action Click Successful',
                'type':'rainbow_man',
                }
            }
