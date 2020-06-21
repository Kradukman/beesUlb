from odoo import api, fields, models, _


class InsectNesting(models.Model):
    _name = 'insect.nesting'
    _description = 'Insect Nesting'

    name = fields.Char('Name', required=True)


class InsectSociality(models.Model):
    _name = 'insect.sociality'
    _description = 'Insect Sociality'

    name = fields.Char('Name', required=True)


class InsectPollenTransport(models.Model):
    _name = 'insect.pollen.transport'
    _description = 'Insect Pollen Transport'

    name = fields.Char('Name', required=True)


class InsectTongue(models.Model):
    _name = 'insect.tongue'
    _description = 'Insect Tongue'

    name = fields.Char('Name', required=True)


class InsectSeason(models.Model):
    _name = 'insect.season'
    _description = 'Insect Season'

    name = fields.Char('Name', required=True)


class InsectLecty(models.Model):
    _name = 'insect.lecty'
    _description = 'Insect Lecty'

    name = fields.Char('Name', required=True)


class InsectDietBreath(models.Model):
    _name = 'insect.diet.breath'
    _description = 'Insect Diet Breath'

    name = fields.Char('Name', required=True)


class InsectEUIUCNStatus(models.Model):
    _name = 'insect.eu.iucn.status'
    _description = 'Insect EU IUCN Status'

    name = fields.Char('Name', required=True)


class InsectBEIUCNStatus(models.Model):
    _name = 'insect.be.iucn.status'
    _description = 'Insect BE IUCN Status'

    name = fields.Char('Name', required=True)


class InsectIntroduced(models.Model):
    _name = 'insect.introduced'
    _description = 'Insect Introduced'

    name = fields.Char('Name', required=True)


class InsectSpecie(models.Model):
    _name = 'insect.specie'
    _description = 'Insect Specie'

    name_display = fields.Char('Insect Binomial Name', compute='_compute_name_display', store=True)
    name = fields.Char('Insect Specie Name', default='', required=True)
    genus_id = fields.Many2one('insect.genus', string='Genus', required=True)
    tribe_id = fields.Many2one(string='Tribe', related='genus_id.tribe_id', readonly=True)
    sub_family_id = fields.Many2one(string='Sub Family', related='genus_id.sub_family_id', readonly=True)
    family_id = fields.Many2one(string='Family', related='sub_family_id.family_id', readonly=True)
    super_family_id = fields.Many2one(string='Super Family', related='family_id.super_family_id')

    itd = fields.Float('ITD')

    nesting_id = fields.Many2one('insect.nesting', string='Nesting')
    sociality_id = fields.Many2one('insect.sociality', string='Sociality')
    pollen_transport_id = fields.Many2one('insect.pollen.transport', string='Pollen Transport')
    tongue_id = fields.Many2one('insect.tongue', string='Tongue')
    season_id = fields.Many2one('insect.season', string='Season')
    lecty_id = fields.Many2one('insect.lecty', string='Lecty')
    diet_breath_id = fields.Many2one('insect.diet.breath', string='Diet Breath')
    eu_iucn_status_id = fields.Many2one('insect.eu.iucn.status', string='EU IUCN status')
    be_iucn_status_id = fields.Many2one('insect.be.iucn.status', string='BE IUCN status')
    introduced_id = fields.Many2one('insect.introduced', string='Introduced')
    comment = fields.Char('Comment')

    @api.depends('name', 'genus_id.name')
    def _compute_name_display(self):
        for insect in self:
            insect.name_display = '%s %s' % (insect.genus_id.name, insect.name)