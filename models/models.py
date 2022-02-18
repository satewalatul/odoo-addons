# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerInherit(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    in_beta = fields.Boolean(default=False, string="In Beta")

