# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from odoo.addons.base_vat.models.res_partner import ResPartner

class PartnerInherit(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    in_beta = fields.Boolean(default=False, string="In Beta")

    def __init__(self):
        self.env.context = dict(self.env.context)
        self.env.context.update({
            'no_vat_validation': True,
        })

    #@api.constrains('vat', 'country_id')
    #def check_vat_extended(self):
    #    raise Exception("Vikas")
    #    return True

    #ResPartner.check_vat = check_vat_extended
