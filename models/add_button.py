# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.tools import date_utils

import logging
import json
import requests

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    in_beta = fields.Boolean(default=False, string="In Beta")

    def button_function(self):
        _logger.warning("To Beta clicked")

        partner_json = self.partner_id.read()
        data = {"partner": partner_json}

        payload = json.dumps(data, default=date_utils.json_default)

        url = "https://youngmanbeta.com/storeOdooCustomer/"

        headers = {
            'Content-Type': 'application/json'
        }

        _logger.warning("About to make request")

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        _logger.warning("Response: " + response.text)

        response_body = response.json()

        if response.status_code == 201 and response_body['status'] == "success":
            self.in_beta = True
            self.partner_id.in_beta = True
            _logger.warning("CrmLead: " + response.text)
        else:
            _logger.error("CrmLead: " + response.text)
            raise Exception("Failed to create Customer: Status=" + str(response.status_code) + " Body: " + response.text )
