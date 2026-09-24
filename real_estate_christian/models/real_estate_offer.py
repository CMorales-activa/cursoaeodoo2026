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
    property_user_id = fields.Many2one(
        related='property_id.user_id', string='Property Responsible')
    category_id = fields.Many2one(
        related='property_id.category_id', readonly=True
    )

    def action_draft(self):
        self.state = "draft"

    def action_sent(self):
        self.state = "sent"

    def action_accepted(self):
        self.state = "accepted"
        self.property_id.action_reserve()

    def action_rejected(self):
        self.state = "rejected"

    def action_create_contract(self):
        self.ensure_one()
        self.env['real.estate.contract'].create({
            'name': self.property_id.name,
            'property_id':self.property_id.id,
            'tenant_id':self.buyer_id.id,
            'type': 'sell',
            'init_date':fields.Datetime.now(),
        })