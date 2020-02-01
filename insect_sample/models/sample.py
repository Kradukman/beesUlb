from odoo import api, fields, models, _


class InsectSample(models.Model):
    _name = "insect.sample.sample"
    _description = "Insect Sample"

    # TODO add automatic sequence on name 
    name = fields.Char('Insect Sample Name', required=True)
    # INSECT
    specie_id = fields.Many2one('insect.specie', string='Specie')
    genus_id = fields.Many2one('insect.genus', related='specie_id.genus_id', string='Genus', readonly=True)
    family_id = fields.Many2one('insect.family', related='genus_id.family_id', string='Family', readonly=True)
    # PLACE
    place_id = fields.Many2one('place.place')
    country_id = fields.Many2one('res.country', related='place_id.country_id', readonly=True)
    state_id = fields.Many2one('res.country.state', related='place_id.state_id', readonly=True)
    city_id = fields.Many2one('place.city', related='place_id.city_id', readonly=True)
    # PLANT
    plant_id = fields.Many2one('plant.specie', string='Plant specie')
    plant_genus_id = fields.Many2one('plant.genus', related='plant_id.genus_id', string='Plant genus', readonly=True)
    plant_family_id = fields.Many2one('plant.family', related='plant_id.family_id', string='Plant family', readonly=True)