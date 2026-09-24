from odoo import models, fields


class RealEstateVisit(models.Model):
    _name = 'real.estate.visit'
    _description = 'Real Estate Visit'

    property_id = fields.Many2one(
        'real.estate.property', 
        string='Property', 
        required=True)
    date = fields.Datetime(string='Date')
    contact_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Contact')
    state = fields.Selection([
        ('new', 'New'),
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='new')
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="user",
    )
    contact_phone = fields.Char(related='contact_id.phone', string='Contact Phone')
    contact_email = fields.Char(related='contact_id.email', string='Contact Email')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Good'),
        ('2', 'Very Good'),
        ('3', 'Excellent'),
    ], string='Priority', default='0')

    def action_cancel(self):
        self.state = "cancelled"

    def action_done(self):
        self.state = "done"

    def action_plan(self):
        self.state = "planned"

    def action_new(self):
        self.state = "new"