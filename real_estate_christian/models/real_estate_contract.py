from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RealEstateContract(models.Model):
    _name = 'real.estate.contract'
    _description = 'Real Estate Contract'
    _name_unique = models.Constraint(
            'UNIQUE(name)',
            'name must be unique',)
    
    name = fields.Char(string='Name', required=True, copy=False)
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
    amount = fields.Monetary(string="Amount")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    deposit = fields.Monetary(string="Deposit")
    state = fields.Selection([
                ('draft', 'Draft'),
                ('active', 'Active'),
                ('finished', 'Finished'),
                ('canceled', 'Canceled'),
            ], string='State', default='draft')

    duration_days = fields.Integer(
        string="Duration (days)",
        compute="_compute_duration_days",
        store=True,
    )
    days_to_end = fields.Integer(
        string="Days to End",
        compute="_compute_days_to_end",
    )
    has_deposit = fields.Boolean(
        string="Con fianza",
        compute="_compute_has_deposit",
        store=True,
    )
    days_in_progress = fields.Integer(
        string="Days in Progress",
        compute="_compute_days_in_progress",
    )

    @api.depends('init_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.init_date and record.end_date:
                record.duration_days = (record.end_date - record.init_date).days
            else:
                record.duration_days = 0

    def _compute_days_to_end(self):
        for record in self:
            if record.end_date:
                record.days_to_end = (record.end_date.date() - fields.Date.today()).days
            else:
                record.days_to_end = 0

    @api.depends('deposit')
    def _compute_has_deposit(self):
        for record in self:
            record.has_deposit = record.deposit > 0

    def _compute_days_in_progress(self):
        for record in self:
            if record.init_date:
                record.days_in_progress = (fields.Date.today() - record.init_date.date()).days
            else:
                record.days_in_progress = 0

    @api.constrains('init_date', 'end_date')
    def _validation_dates(self):
        for record in self:
            if (record.end_date and record.init_date and
               record.end_date < record.init_date):
                raise ValidationError(_("End date must be bigger tna init date"))
    
    def action_draft(self):
        self.state = "draft"

    def action_activate(self):
        self.state = "active"

    def action_finish(self):
        self.state = "finished"

    def action_cancel(self):
        self.state = "canceled"

    def _cron_finish_contracts(self):
        contracts_to_finish = self.env['real.estate.contract'].search(
            [('state', '=', 'active'),
             ('end_date', '<', fields.Datetime.now())
             ],
        )
        contracts_to_finish.write({'state': 'finished'})

    @api.onchange('property_id')
    def property_changes(self):
        self.amount = self.property_id.price
