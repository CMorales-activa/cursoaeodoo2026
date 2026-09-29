from odoo import api, models, fields, _


class RealEstateProperty(models.TransientModel):
    _name = 'real.estate.property.stage.wizard'
    _description = 'Real Estate Property Wizard'

    property_ids = fields.Many2many('real.estate.property', string='Properties',
    default=lambda self: self.env.context.get('active_ids'))
    stage_id = fields.Many2one(
        'real.estate.property.stage',
        string='Stage',
        required=True,
    )

    def action_apply(self):
        self.property_ids.write({'stage_id': self.stage_id.id})