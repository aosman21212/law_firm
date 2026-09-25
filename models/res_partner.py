# -*- coding: utf-8 -*-

from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_law_client = fields.Boolean(string='Law Firm Client')
    law_case_ids = fields.One2many('law.case', 'client_id', string='Cases')
    law_case_count = fields.Integer(compute='_compute_law_case_count')

    def _compute_law_case_count(self):
        for partner in self:
            partner.law_case_count = self.env['law.case'].search_count(
                [('client_id', '=', partner.id)])

    def action_view_law_cases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cases'),
            'res_model': 'law.case',
            'view_mode': 'list,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }
