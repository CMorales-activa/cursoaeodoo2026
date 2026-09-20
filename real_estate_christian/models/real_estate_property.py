from odoo import models, fields


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
    )
    category_id = fields.Many2one('real.estate.category', string='Category')

    def action_reserve(self):
        self.availability = False
