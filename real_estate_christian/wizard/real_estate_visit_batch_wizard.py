from odoo import api, models, fields, _
from datetime import timedelta


class RealEstateProperty(models.TransientModel):
    _name = 'real.estate.property.batch.wizard'
    _description = 'Real Estate Property Wizard'

    property_id = fields.Many2one('real.estate.property', string='Property',
    default=lambda self: self.env.context.get('active_id'))
    date_from = fields.Datetime(string='Date from')
    date_to = fields.Datetime(string='Date to')
    

    def action_apply(self):
        num_days = (self.date_to - self.date_from).days
        for i in range(num_days + 1):
            visit_date = self.date_from + timedelta(days=i)
            self.env['real.estate.visit'].create({
                'property_id': self.property_id.id,
                'date': visit_date,
                'state': 'planned',
                'user_id': self.property_id.user_id.id,
            })
