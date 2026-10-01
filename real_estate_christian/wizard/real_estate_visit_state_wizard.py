from odoo import api, models, fields, _


class RealEstateVisitStateWizard(models.TransientModel):
    _name = 'real.estate.visit.stage.wizard'
    _description = 'Real Estate Visit Wizard'

    visit_ids = fields.Many2many('real.estate.visit', string='Visits',
    default=lambda self: self.env.context.get('active_ids'))
    state = fields.Selection([
            ('new', 'New'),
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ], string='State', default='new')

    def action_apply(self):
        self.visit_ids.write({'state': self.state})