from odoo import api, fields, models, _


class PlacePlace(models.Model):
    _name = "place.place"
    _description = "Place Place"

    name = fields.Char('Name', required=True)
    date_of_sampling_ids = fields.Many2many('place.date.of.sampling', string='Date of sampling')
    owner_id = fields.Many2one('res.partner', string='Owner')
    city_id = fields.Many2one('place.city', string='City')
    state_id = fields.Many2one('res.country.state', related='city_id.state_id', string='State', readonly=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', string='Country', readonly=True)
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')