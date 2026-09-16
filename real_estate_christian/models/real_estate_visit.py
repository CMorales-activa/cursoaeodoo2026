from odoo import models, fields


class RealEstateVisit(models.Model):
    _name = 'real.estate.visit'
    _description = 'Real Estate Visit'

    property_id = fields.Many2one('real.estate.property', string='Property', required=True)
    date = fields.Datetime(string='Date')
    contact_id = fields.Many2one('res.partner', string='Contact')
    state = fields.Selection([
        ('new', 'New'),
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='new')
