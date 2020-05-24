from odoo import api, fields, models, _


class InsectSex(models.Model):
    _name = "insect.sample.sex"
    _description = 'Insect Sample Sex'

    name = fields.Char('Insect sex')


class InsectTrap(models.Model):
    _name = "insect.sample.trap"
    _description = "Insect Sample Trap"

    name = fields.Char('Name', required=True)


class InsectPhysicalStatus(models.Model):
    _name = "insect.sample.physical.status"
    _description = "Insect Sample Physical status"

    name = fields.Char('Name', required=True)


class InsectCollectionStatus(models.Model):
    _name = "insect.sample.collection.status"
    _description = "Insect Sample Collection status"

    name = fields.Char('Name', required=True)


class InsectIDStatus(models.Model):
    _name = "insect.sample.id.status"
    _description = "Insect Sample ID status"

    name = fields.Char('Name', required=True)


class InsectSample(models.Model):
    _name = "insect.sample.sample"
    _description = "Insect Sample"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # TODO add automatic sequence on name 
    name = fields.Char('Insect Sample Name', compute='_compute_name', store=True)
    legacy_name = fields.Char('Insect legacy name', default=False)
    # INSECT
    specie_id = fields.Many2one('insect.specie', string='Specie')
    genus_id = fields.Many2one('insect.genus', related='specie_id.genus_id', string='Genus', readonly=True)
    subspecie_id = fields.Many2one('insect.subspecie', string='Subspecie')
    
    # PLACE
    place_id = fields.Many2one('place.place', required=True)
    country_id = fields.Many2one('res.country', related='place_id.country_id', readonly=True)
    state_id = fields.Many2one('res.country.state', related='place_id.state_id', readonly=True)
    city_id = fields.Many2one('place.city', related='place_id.city_id', readonly=True)

    # PLANT
    plant_id = fields.Many2one('plant.specie', string='Plant specie')
    plant_genus_id = fields.Many2one('plant.genus', related='plant_id.genus_id', string='Plant genus', readonly=True)
    plant_family_id = fields.Many2one('plant.family', related='plant_id.family_id', string='Plant family', readonly=True)

    # PROJECT
    project_id = fields.Many2one('project_ulb.project', string='Project', required=True)
    year = fields.Date('Year', related='project_id.year', readonly=True)
    project_leader_ids = fields.Many2many('res.partner', string='Project leader', related='project_id.leader_ids', readonly=True)

    # SAMPLE
    identifier_id = fields.Many2one('res.partner', string='Identifier')
    sex_id = fields.Many2one('insect.sample.sex', string='Sex')
    trap_id = fields.Many2one('insect.sample.trap', string='Trap', required=True)
    physical_status_id = fields.Many2one('insect.sample.physical.status', string='Physical Status', required=True)
    collection_status_id = fields.Many2one('insect.sample.collection.status', string='Collection Status')
    id_status_id = fields.Many2one('insect.sample.id.status', string='ID Status', required=True)
    sampling_date = fields.Date('Sampling Date', required=True) # Use domain to filter on view

    remark = fields.Char('Remark')

    is_validated = fields.Boolean('Has been validated', groups='base.group_erp_manager')
    sampler_id = fields.Many2one('res.partner', string='Sampler', default=lambda self: self.env.user.partner_id, required=True)

    # add inherit chatter
    @api.depends('sampler_id', 'sampling_date')
    def _compute_name(self):
        # id - annee - sampler - projet
        for sample in self:
            if sample.legacy_name:
                sample.name = sample.legacy_name
            else:
                sample.name = ''
                if isinstance(sample.id, int):
                    sample.name = '%d' %sample.id
                if sample.sampler_id:
                    sample.name = '%s - %s' %(sample.name, sample.sampler_id.name)
