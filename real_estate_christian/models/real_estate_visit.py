from odoo import models, fields, api


class RealEstateVisit(models.Model):
    _name = 'real.estate.visit'
    _description = 'Real Estate Visit'

    property_id = fields.Many2one(
        'real.estate.property', 
        string='Property', 
        required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
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
    contact_phone = fields.Char(string='Contact Phone')
    contact_email = fields.Char(string='Contact Email')
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

    @api.onchange('contact_id')
    def contact_changes(self):
        self.contact_phone = self.contact_id.phone
        self.contact_email = self.contact_id.email

    def _cron_done_visits(self):
        visits_to_done = self.env['real.estate.visit'].search([
            ('state', '=', 'planned'),
            ('date', '<', fields.Datetime.now()),
        ])
        visits_to_done.write({'state': 'done'})