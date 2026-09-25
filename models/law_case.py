# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LawCase(models.Model):
    _name = 'law.case'
    _description = 'Legal Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date_open desc, id desc'

    # ---------- Identification ----------
    name = fields.Char(
        string='Case Reference', required=True, copy=False,
        readonly=True, default=lambda self: _('New'))
    title = fields.Char(string='Case Title', required=True, tracking=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()
    priority = fields.Selection([
        ('0', 'Normal'), ('1', 'High'), ('2', 'Urgent'),
    ], default='0', tracking=True)

    # ---------- Parties ----------
    client_id = fields.Many2one(
        'res.partner', string='Client', required=True, tracking=True)
    opposing_party = fields.Char()
    opposing_lawyer = fields.Char()

    # ---------- Team ----------
    lawyer_id = fields.Many2one(
        'res.users', string='Responsible Lawyer', tracking=True,
        default=lambda self: self.env.user)
    assistant_ids = fields.Many2many('res.users', string='Case Team')

    # ---------- Classification ----------
    case_type_id = fields.Many2one('law.case.type', string='Case Type', tracking=True)
    court_id = fields.Many2one('law.court', string='Court', tracking=True)

    # ---------- Dates & status ----------
    date_open = fields.Date(
        string='Opening Date', default=fields.Date.context_today, tracking=True)
    date_close = fields.Date(string='Closing Date', readonly=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', required=True, tracking=True, copy=False)
    outcome = fields.Selection([
        ('won', 'Won'), ('lost', 'Lost'),
        ('settled', 'Settled'), ('withdrawn', 'Withdrawn'),
    ], tracking=True, copy=False)
    description = fields.Html()

    # ---------- Fees ----------
    fee_type = fields.Selection([
        ('fixed', 'Fixed Fee'), ('hourly', 'Hourly'), ('contingency', 'Contingency'),
    ], default='fixed')
    fee_amount = fields.Monetary(currency_field='currency_id')
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True)

    # ---------- Hearings ----------
    hearing_ids = fields.One2many('law.hearing', 'case_id', string='Hearings')
    hearing_count = fields.Integer(compute='_compute_hearing_info')
    next_hearing_date = fields.Datetime(compute='_compute_hearing_info')

    @api.depends('hearing_ids.date_hearing', 'hearing_ids.state')
    def _compute_hearing_info(self):
        now = fields.Datetime.now()
        for case in self:
            case.hearing_count = len(case.hearing_ids)
            upcoming = case.hearing_ids.filtered(
                lambda h: h.state == 'scheduled' and h.date_hearing and h.date_hearing >= now)
            case.next_hearing_date = min(upcoming.mapped('date_hearing')) if upcoming else False

    # ---------- ORM overrides ----------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('law.case') or _('New')
        return super().create(vals_list)

    def unlink(self):
        if any(case.state not in ('draft', 'cancelled') for case in self):
            raise UserError(_('You can only delete cases in Draft or Cancelled state.'))
        return super().unlink()

    # ---------- Button actions ----------
    def action_open(self):
        self.write({'state': 'open'})

    def action_hold(self):
        self.write({'state': 'on_hold'})

    def action_close(self):
        for case in self:
            if not case.outcome:
                raise UserError(_('Please set the case outcome before closing %s.', case.name))
        self.write({'state': 'closed', 'date_close': fields.Date.context_today(self)})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft', 'date_close': False})

    def action_view_hearings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hearings'),
            'res_model': 'law.hearing',
            'view_mode': 'list,calendar,form',
            'domain': [('case_id', '=', self.id)],
            'context': {'default_case_id': self.id},
        }
