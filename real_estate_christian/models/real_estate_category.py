from odoo import models, fields


class RealEstateCategory(models.Model):
    _name = 'real.estate.category'
    _description = 'Real Estate Category'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')