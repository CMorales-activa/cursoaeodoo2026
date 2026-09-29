from odoo import api, models, fields, _


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'
    _reference_unique = models.Constraint(
        'UNIQUE(reference)',
        'reference must be unique',)

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Monetary(string="Price")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    reference = fields.Char(string="Reference", copy=False)
    availability = fields.Boolean(string="Availability", default=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company',
                                  string='Company',
                                  default=lambda self: self.env.company)
    internal_note = fields.Text(string='Internal Note',
                                 company_dependent=True)
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
    offer_ids = fields.One2many(
        'real.estate.offer', 'property_id', string='Offers'
    )
    next_visit_date = fields.Datetime(
        string='Next Visit Date', compute='_compute_next_visit_date')
    visit_count = fields.Integer(
        string='Visits count', compute='_compute_visits_count_')
    incidence_count = fields.Integer(
        string='Incidence count', compute='_compute_incidence_count_')


    @api.depends('visit_ids')
    def _compute_visits_count_(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    @api.depends('incidence_ids')
    def _compute_incidence_count_(self):
        for record in self:
            record.incidence_count = len(record.incidence_ids)

    @api.depends('visit_ids.date', 'visit_ids.state')
    def _compute_next_visit_date(self):
        for record in self:
            planned_visits = record.visit_ids.filtered(
                lambda v: v.state == 'planned')
            if planned_visits:
                record.next_visit_date = min(planned_visits.mapped('date'))
            else:
                record.next_visit_date = False

    def action_reserve(self):
        self.availability = False

    def action_create_visit(self):
        self.ensure_one()
        self.env['real.estate.visit'].create({
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'user_id': self.user_id.id,
        })

    def action_view_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'real.estate.visit',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
        }

    def action_view_incidences(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incidences',
            'res_model': 'real.estate.property.incidence',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
        }
    
    def action_accept_best_offer(self):
        self.ensure_one()
        best_offer = self.env['real.estate.offer'].search(
            [('property_id', '=', self.id), ('state', '=', 'sent')],
            order='amount desc',
            limit=1,
        )
        if best_offer:
            best_offer.action_accepted()

    def action_cancel_visits(self):
        self.ensure_one()
        visits_to_cancel = self.env['real.estate.visit'].search(
            [('property_id', '=', self.id), ('state', 'in', ('new', 'planned'))],
        )
        visits_to_cancel.write({'state': 'cancelled'})

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

    def action_open_visit_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visits',
            'res_model': 'real.estate.property.batch.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_property_id': self.id},
        }
