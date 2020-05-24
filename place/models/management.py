from odoo import api, fields, models, _


class PlaceManagement(models.Model):
    _name = "place.management"
    _description = "Place Management"

    name = fields.Char('Name', required=True)