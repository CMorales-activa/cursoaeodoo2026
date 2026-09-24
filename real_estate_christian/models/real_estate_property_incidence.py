from odoo import fields, models


class RealEstatePropertyIncidence(models.Model):
    _name = 'real.estate.property.incidence'
    _description = 'Real Estate Property Incidence'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='0')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='new')
    date = fields.Datetime(string='Date')
    user_id = fields.Many2one('res.users', string='Assigned User')
    property_id = fields.Many2one(
        'real.estate.property', string='Property', required=True, ondelete='cascade')
