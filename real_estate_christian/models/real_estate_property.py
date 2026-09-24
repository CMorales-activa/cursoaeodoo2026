from odoo import models, fields


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
    )
    category_id = fields.Many2one('real.estate.category', string='Category')
    stage_id = fields.Many2one(
        'real.estate.property.stage',
        string='Stage',
        default=lambda self: self.env['real.estate.property.stage'].search(
            [], order='sequence, id', limit=1),
    )
    image_ids = fields.One2many(
        'real.estate.property.image', 'property_id', string='Images')
    visit_ids = fields.One2many(
        'real.estate.visit', 'property_id', string='Visits')
    incidence_ids = fields.One2many(
        'real.estate.property.incidence', 'property_id', string='Incidences')

    def action_reserve(self):
        self.availability = False

    def action_create_visit(self):
        self.ensure_one()
        self.env['real.estate.visit'].create({
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'user_id': self.user_id.id,
        })

    def action_accept_best_offer(self):
        self.ensure_one()
        best_offer = self.env['real.estate.offer'].search(
            [('property_id', '=', self.id), ('state', '=', 'sent')],
            order='amount desc',
            limit=1,
        )
        if best_offer:
            best_offer.action_accepted()

    def action_delete_rejected_offers(self):
        self.ensure_one()
        rejected_offers = self.env['real.estate.offer'].search([
            ('property_id', '=', self.id),
            ('state', '=', 'rejected'),
        ])
        rejected_offers.unlink()

    def action_create_offer(self):
        self.ensure_one()
        self.env['real.estate.offer'].create({
            'property_id': self.id,
            'amount': self.price,
            'state': 'draft',
        })
