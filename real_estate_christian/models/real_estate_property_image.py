from odoo import fields, models


class RealEstatePropertyImage(models.Model):
    _name = 'real.estate.property.image'
    _description = 'Real Estate Property Image'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    image = fields.Binary(string='Image')
    sequence = fields.Integer(string='Sequence', default=10)
    property_id = fields.Many2one(
        'real.estate.property', string='Property', required=True, ondelete='cascade')
