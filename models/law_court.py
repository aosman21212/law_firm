# -*- coding: utf-8 -*-

from odoo import fields, models


class LawCourt(models.Model):
    _name = 'law.court'
    _description = 'Court'
    _order = 'name'

    name = fields.Char(string='Court Name', required=True)
    court_type = fields.Selection([
        ('general', 'General Court'),
        ('criminal', 'Criminal Court'),
        ('commercial', 'Commercial Court'),
        ('labor', 'Labor Court'),
        ('family', 'Family Court'),
        ('appeal', 'Court of Appeal'),
        ('supreme', 'Supreme Court'),
    ], default='general')
    city = fields.Char()
    address = fields.Text()
    phone = fields.Char()
    active = fields.Boolean(default=True)
