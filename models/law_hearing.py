# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LawHearing(models.Model):
    _name = 'law.hearing'
    _description = 'Court Hearing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_hearing desc'

    name = fields.Char(string='Subject', required=True, tracking=True)
    case_id = fields.Many2one(
        'law.case', string='Case', required=True, ondelete='cascade', tracking=True)
    client_id = fields.Many2one(related='case_id.client_id', store=True)
    court_id = fields.Many2one(
        'law.court', compute='_compute_from_case', store=True, readonly=False)
    lawyer_id = fields.Many2one(
        'res.users', string='Lawyer', compute='_compute_from_case',
        store=True, readonly=False)
    date_hearing = fields.Datetime(string='Hearing Date', required=True, tracking=True)
    duration = fields.Float(default=1.0, help='Duration in hours')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('postponed', 'Postponed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled', required=True, tracking=True)
    notes = fields.Html(string='Preparation Notes')
    result = fields.Text(string='Hearing Result')

    @api.depends('case_id')
    def _compute_from_case(self):
        for hearing in self:
            hearing.court_id = hearing.case_id.court_id
            hearing.lawyer_id = hearing.case_id.lawyer_id

    def action_done(self):
        self.write({'state': 'done'})

    def action_postpone(self):
        self.write({'state': 'postponed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reschedule(self):
        self.write({'state': 'scheduled'})
