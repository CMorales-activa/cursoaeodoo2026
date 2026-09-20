from odoo import models, fields


class RealEstateContract(models.Model):
    _name = 'real.estate.contract'
    _description = 'Real Estate Contract'

    name = fields.Char(string='Name', required=True)
    type = fields.Selection([
            ('sell', 'Sell'),
            ('rent', 'Rent'),
        ], string='Type', default='rent')
    property_id = fields.Many2one('real.estate.property', string='Property')
    tenant_id = fields.Many2one(
                comodel_name='res.partner', 
                string='Tenant')
    init_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    amount = fields.Float(string="Amount")
    deposit = fields.Float(string="Deposit")
    state = fields.Selection([
                ('draft', 'Draft'),
                ('active', 'Active'),
                ('finished', 'Finished'),
                ('canceled', 'Canceled'),
            ], string='State', default='draft')

    def action_activate(self):
        self.state = "active"

    def action_finish(self):
        self.state = "finished"

    def action_cancel(self):
        self.state = "canceled"
