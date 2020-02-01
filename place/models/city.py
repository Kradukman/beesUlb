from odoo import api, fields, models, _


class PlaceCity(models.Model):
    _name = "place.city"
    _description = "City"

    name = fields.Char('City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', related='state_id.country_id', readonly=True)