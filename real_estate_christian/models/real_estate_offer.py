from odoo import models, fields


class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = 'Real Estate Offer'

    property_id = fields.Many2one('real.estate.property', string='Property')
    buyer_id = fields.Many2one(
            comodel_name='res.partner', 
            string='Buyer')
    amount = fields.Float(string="Amount")
    date = fields.Datetime(string='Date')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ], string='State', default='draft')
    notes = fields.Text(string='Description')

    def action_draft(self):
        self.state = "draft"

    def action_sent(self):
        self.state = "sent"

    def action_accepted(self):
        self.state = "accepted"
        self.property_id.action_reserve()

    def action_rejected(self):
        self.state = "rejected"
