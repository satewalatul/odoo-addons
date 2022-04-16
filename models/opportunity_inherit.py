# -*- coding: utf-8 -*-

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    in_beta = fields.Boolean(default=False, string="In Beta")
    job_order = fields.Char(string="Job Order")

    def button_function(self):
        self.in_beta = True
        self.partner_id.in_beta = True
