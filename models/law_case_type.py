# -*- coding: utf-8 -*-

from odoo import fields, models


class LawCaseType(models.Model):
    _name = 'law.case.type'
    _description = 'Case Type'
    _order = 'sequence, name'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This case type already exists!'),
    ]
