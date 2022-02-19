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
        lead_json = self.read()

        payload = json.dumps({"partner": partner_json, "lead": lead_json}, default=date_utils.json_default)

        _logger.warning("Payload: "+ payload)

        url = "https://3c7b-103-206-129-194.ngrok.io/storeOdooCustomer"

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_body = json.loads(response.json())

        if response.status_code == 201 and response_body['status'] == "success":
            self.in_beta = True
            self.partner_id.in_beta = True
            _logger.warning("CrmLead: " + response.json())
        else:
            _logger.error("CrmLead: " + response.json())
            return {
                'warning': {'title': 'Warning',
                            'message': 'Failed to send Lead data to Beta', },
            }
