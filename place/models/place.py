from odoo import api, fields, models, _


class PlacePlace(models.Model):
    _name = "place.place"
    _description = "Place Place"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    date_of_sampling_ids = fields.Many2many('place.date.of.sampling', string='Date of sampling')
    owner_id = fields.Many2one('res.partner', string='Owner')
    city_id = fields.Many2one('place.city', string='City', required=True)
    state_id = fields.Many2one('res.country.state', related='city_id.state_id', string='State', readonly=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', string='Country', readonly=True)
    country_code = fields.Char('Country Code', related='country_id.code', readonly=True)
    latitude = fields.Float('Latitude', required=True)
    longitude = fields.Float('Longitude', required=True)
    type_id = fields.Many2one('place.type', string='Type')
    crop_id = fields.Many2one('place.crop', string='Crop')
    management_id = fields.Many2one('place.management', string='Management')
    cultivar_ids = fields.Many2many('place.cultivar', string='Cultivar')