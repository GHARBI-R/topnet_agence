# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    role = fields.Selection([("administrateur", "Administrateur"), ("responsable agences", "Responsable agences"),
                             ("chef agence", "Chef agence"), ("agent", "Agent")], required=True)


