from odoo import api, fields, models, _


class InsectSample(models.Model):
    _name = "insect.sample.sample"
    _description = "Insect Sample"

    # TODO add automatic sequence on name 
    name = fields.Char('Insect Sample Name', compute='_compute_name')
    # INSECT
    specie_id = fields.Many2one('insect.specie', string='Specie')
    genus_id = fields.Many2one('insect.genus', related='specie_id.genus_id', string='Genus', readonly=True)
    family_id = fields.Many2one('insect.family', related='genus_id.family_id', string='Family', readonly=True)
    # PLACE
    place_id = fields.Many2one('place.place')
    country_id = fields.Many2one('res.country', related='place_id.country_id', readonly=True)
    state_id = fields.Many2one('res.country.state', related='place_id.state_id', readonly=True)
    city_id = fields.Many2one('place.city', related='place_id.city_id', readonly=True)
    sampling_date = fields.Many2one('place.date.of.sampling') # Use domain to filter on view
    # PLANT
    plant_id = fields.Many2one('plant.specie', string='Plant specie')
    plant_genus_id = fields.Many2one('plant.genus', related='plant_id.genus_id', string='Plant genus', readonly=True)
    plant_family_id = fields.Many2one('plant.family', related='plant_id.family_id', string='Plant family', readonly=True)

    is_validated = fields.Boolean('Has been validated', groups='base.group_erp_manager')
    sampler_id = fields.Many2one('res.users', string='Sampler', default=lambda self: self.env.user)

    @api.depends('sampler_id', 'sampling_date')
    def _compute_name(self):
        for sample in self:
            sample.name = ''
            if isinstance(sample.id, int):
                sample.name = '%d' %sample.id
            if sample.sampler_id:
                sample.name = '%s - %s' %(sample.name, sample.sampler_id.name)