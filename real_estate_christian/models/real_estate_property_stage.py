from odoo import fields, models


class RealEstatePropertyStage(models.Model):
    _name = 'real.estate.property.stage'
    _description = 'Real Estate Property Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
