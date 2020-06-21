from odoo import api, fields, models, _
import csv
import io
import base64


class ImportWizard(models.TransientModel):
    _name = 'insect.import.wizard'
    _description = 'Import wizard'

    csv_file = fields.Binary('csv file to import', required=True)
    start_line = fields.Integer('Start line', default=2, required=True)
    separator = fields.Char('Separator', default=',', required=True)
    error_message = fields.Text('Message', readonly=True)
    has_super_family = fields.Boolean('Super family', default=False)
    super_family_col = fields.Integer('Super Family Name column number', default=2)
    has_family = fields.Boolean('Family', default=False)
    family_col = fields.Integer('Family Name column number', default=4)
    has_position = fields.Boolean('Position', default=False)
    position_col = fields.Integer('Position column number', default=3)
    has_sub_family = fields.Boolean('Sub family', default=False)
    sub_family_col = fields.Integer('Sub Family Name column number', default=5)
    has_tribe = fields.Boolean('Tribe', default=False)
    tribe_col = fields.Integer('Tribe Name column number', default=6)
    has_genus = fields.Boolean('Genus', default=False)
    genus_col = fields.Integer('Genus Name column number', default=7)
    has_specie = fields.Boolean('Specie', default=False)
    specie_col = fields.Integer('Specie Name column number', default=9)
    has_sub_specie = fields.Boolean('Sub Specie', default=False)
    sub_specie_col = fields.Integer('Sub Specie Name column number', default=9)
    #specie fields
    has_itd = fields.Boolean('itd', default=False)
    itd_col = fields.Integer('itd column numer', default=10)
    has_nesting = fields.Boolean('nesting', default=False)
    nesting_col = fields.Integer('nesting column number', default=11)
    has_sociality = fields.Boolean('sociality', default=False)
    sociality_col = fields.Integer('sociality column number', default=12)
    has_pollen_transport = fields.Boolean('pollen_transport', default=False)
    pollen_transport_col = fields.Integer('pollen_transport column number', default=13)
    has_tongue = fields.Boolean('tongue', default=False)
    tongue_col = fields.Integer('tongue column number', default=14)
    has_season = fields.Boolean('season', default=False)
    season_col = fields.Integer('season column number', default=15)
    has_lecty = fields.Boolean('lecty', default=False)
    lecty_col = fields.Integer('lecty column number', default=16)
    has_diet_breath = fields.Boolean('diet_breath', default=False)
    diet_breath_col = fields.Integer('diet_breath column number', default=17)
    has_eu_iucn_status = fields.Boolean('eu_iucn_status', default=False)
    eu_iucn_status_col = fields.Integer('eu_iucn_status column number', default=18)
    has_be_iucn_status = fields.Boolean('be_iucn_status', default=False)
    be_iucn_status_col = fields.Integer('be_iucn_status column number', default=19)
    has_introduced = fields.Boolean('introduced', default=False)
    introduced_col = fields.Integer('introduced column number', default=20)
    has_comment = fields.Boolean('comment', default=False)
    comment_col = fields.Integer('comment column number')

    @api.onchange('has_specie')
    def onchange_specie(self):
        if self.has_specie:
            self.has_itd = True
            self.has_nesting = True
            self.has_sociality = True
            self.has_pollen_transport = True
            self.has_tongue = True
            self.has_season = True
            self.has_lecty = True
            self.has_diet_breath = True
            self.has_eu_iucn_status = True
            self.has_be_iucn_status = True
            self.has_introduced = True
            self.has_comment = True
            self.has_genus = True
            self.onchange_genus()
        else:
            self.has_itd = False
            self.has_nesting = False
            self.has_sociality = False
            self.has_pollen_transport = False
            self.has_tongue = False
            self.has_season = False
            self.has_lecty = False
            self.has_diet_breath = False
            self.has_eu_iucn_status = False
            self.has_be_iucn_status = False
            self.has_introduced = False
            self.has_comment = False

    @api.onchange('has_super_family')
    def onchange_super_family(self):
        if not self.has_family:
            self.has_sub_family = False
            self.onchange_sub_family

    @api.onchange('has_family')
    def onchange_family(self):
        if self.has_family:
            self.has_super_family = True
            self.onchange_super_family()
        else:
            self.has_sub_family = False
            self.onchange_sub_family

    @api.onchange('has_sub_family')
    def onchange_sub_family(self):
        if self.has_sub_family:
            self.has_family = True
            self.onchange_family()
        else:
            self.has_genus = False
            self.onchange_genus

    @api.onchange('has_genus')
    def onchange_genus(self):
        if self.has_genus:
            self.has_sub_family = True
            self.onchange_sub_family()
        else:
            self.has_specie = False
            self.onchange_specie

    @api.onchange('has_genus')
    def onchange_tribe(self):
        if self.has_tribe:
            self.has_sub_family = True
            self.onchange_sub_family()

    @api.onchange('has_sub_specie')
    def onchange_sub_specie(self):
        if self.has_sub_specie:
            self.has_specie = True
            self.onchange_specie()
        else:
            self.has_specie = False

    def action_import(self):
        self.ensure_one()
        unimported_lines = ''
        i = 1
        with io.BytesIO(base64.b64decode(self.csv_file)) as f:
            for line in f.getvalue().splitlines():
                if i >= self.start_line:
                    if len(line) > 0:
                        is_import_successful, message = self.import_line(line)
                        if not is_import_successful:
                            unimported_lines += 'line %s: error: %s \n' %(i + 1, message)
                i = i + 1
        if not unimported_lines:
            self.error_message = 'All lines imported successfully'
        else:
            self.error_message = ('unimported lines: \n %s' % unimported_lines)

    def import_line(self, line):
        is_import_successful = True
        message = ''
        split = line.split(self.separator.encode())

        # INITIALIZATION
        super_family_id = False
        super_family_model = 'insect.super.family'
        super_family_field = 'super_family_id'
        family_id = False
        family_model = 'insect.family'
        family_field = 'family_id'
        position = False
        sub_family_id = False
        sub_family_model = 'insect.sub.family'
        sub_family_field = 'sub_family_id'
        tribe_id = False
        tribe_model = 'insect.tribe'
        tribe_field = 'tribe_id'
        genus_id = False
        genus_model = 'insect.genus'
        genus_field = 'genus_id'
        specie_id = False
        specie_model = 'insect.specie'
        specie_field = 'specie_id'
        sub_specie_id = False
        sub_specie_model = 'insect.sub.specie'
        sub_specie_field = 'sub_specie_id'

        #  specie sub field init
        nesting_id = False
        nesting_model = 'insect.nesting'
        nesting_field = 'nesting_id'
        sociality_id = False
        sociality_model = 'insect.sociality'
        sociality_field = 'sociality_id'
        pollen_transport_id = False
        pollen_transport_model = 'insect.pollen.transport'
        pollen_transport_field = 'pollen_transport_id'
        tongue_id = False
        tongue_model = 'insect.tongue'
        tongue_field = 'tongue_id'
        season_id = False
        season_model = 'insect.season'
        season_field = 'season_id'
        lecty_id = False
        lecty_model = 'insect.lecty'
        lecty_field = 'lecty_id'
        diet_breath_id = False
        diet_breath_model = 'insect.diet.breath'
        diet_breath_field = 'diet_breath_id'
        eu_iucn_status_id = False
        eu_iucn_status_model = 'insect.eu.iucn.status'
        eu_iucn_status_field = 'eu_iucn_status_id'
        be_iucn_status_id = False
        be_iucn_status_model = 'insect.be.iucn.status'
        be_iucn_status_field = 'be_iucn_status_id'
        introduced_id = False
        introduced_model = 'insect.introduced'
        introduced_field = 'introduced_id'

        # PREPROCESS
        if self.has_super_family:
            super_family_name = split[self.super_family_col - 1].decode('utf-8')
        if self.has_family:
            family_name = split[self.family_col - 1].decode('utf-8')
        if self.has_position:
            position = split[self.position_col - 1].decode('utf-8')
        if self.has_sub_family:
            sub_family_name = split[self.sub_family_col - 1].decode('utf-8')
        if self.has_tribe:
            tribe_name = split[self.tribe_col - 1].decode('utf-8')
        if self.has_genus:
            genus_name = split[self.genus_col - 1].decode('utf-8')
        if self.has_specie:
            specie_name = split[self.specie_col - 1].decode('utf-8')
        if self.has_sub_specie:
            sub_specie_name = split[self.sub_specie_col - 1].decode('utf-8')
        # specie sub fields pre process
        if self.has_itd:
            itd = split[self.itd_col - 1].decode('utf-8')
        if self.has_nesting:
            nesting_name = split[self.nesting_col - 1].decode('utf-8')
        if self.has_sociality:
            sociality_name = split[self.sociality_col - 1].decode('utf-8')
        if self.has_pollen_transport:
            pollen_transport_name = split[self.pollen_transport_col - 1].decode('utf-8')
        if self.has_tongue:
            tongue_name = split[self.tongue_col - 1].decode('utf-8')
        if self.has_season:
            season_name = split[self.season_col - 1].decode('utf-8')
        if self.has_lecty:
            lecty_name = split[self.lecty_col - 1].decode('utf-8')
        if self.has_diet_breath:
            diet_breath_name = split[self.diet_breath_col - 1].decode('utf-8')
        if self.has_eu_iucn_status:
            eu_iucn_status_name = split[self.eu_iucn_status_col - 1].decode('utf-8')
        if self.has_be_iucn_status:
            be_iucn_status_name = split[self.be_iucn_status_col - 1].decode('utf-8')
        if self.has_introduced:
            introduced_name = split[self.introduced_col - 1].decode('utf-8')
        if self.has_comment:
            comment = split[self.comment_col - 1].decode('utf-8')

        # IMPORT
        # Insect
        if self.has_super_family:
            super_family_id = self.get_or_create_element(super_family_name, super_family_model)
            if not super_family_id:
                is_import_successful = False
                message = 'super family error'

        if self.has_family:
            if not super_family_id:
                is_import_successful = False
                message += 'super family required'
            else:
                family_id = self.get_or_create_element_with_parent(
                    super_family_id, super_family_field, family_name, family_model)
                if not family_id:
                    is_import_successful = False
                    message = 'Family'
                if family_id and position:
                    family_id.position = position

        if self.has_sub_family:
            if not family_id:
                is_import_successful = False
                message += 'Family required'
            else:
                sub_family_id = self.get_or_create_element_with_parent(
                    family_id, family_field, sub_family_name, sub_family_model)
                if not family_id:
                    is_import_successful = False
                    message = 'Sub Family'

        if self.has_tribe:
            if not sub_family_id:
                is_import_successful = False
                message += 'Sub Family required'
            else:
                tribe_id = self.get_or_create_element_with_parent(
                    sub_family_id, sub_family_field, tribe_name, tribe_model)
                if not tribe_id and tribe_name:
                    is_import_successful = False
                    message = 'Tribe'

        if self.has_genus:
            if not sub_family_id:
                is_import_successful = False
                message += 'Sub Family required'
            else:
                genus_id = self.get_or_create_element_with_parent(
                    sub_family_id, sub_family_field, genus_name, genus_model)
                if not genus_id:
                    is_import_successful = False
                    message = 'Genus'
                if genus_id and tribe_id:
                    genus_id.tribe_id = tribe_id

        if self.has_specie:
            if not genus_id:
                is_import_successful = False
                message += 'Genus required'
            else:
                specie_id = self.get_or_create_element_with_parent(
                    genus_id, genus_field, specie_name, specie_model)
                if not specie_id:
                    is_import_successful = False
                    message = 'Specie'
                if specie_id and itd:
                    specie_id.itd = itd
                if specie_id:
                    if self.has_nesting:
                        nesting_id = self.get_or_create_element(nesting_name, nesting_model)
                        if nesting_id:
                            specie_id.nesting_id = nesting_id
                    if self.has_sociality:
                        sociality_id = self.get_or_create_element(sociality_name, sociality_model)
                        if sociality_id:
                            specie_id.sociality_id = sociality_id
                    if self.has_pollen_transport:
                        pollen_transport_id = self.get_or_create_element(pollen_transport_name, pollen_transport_model)
                        if pollen_transport_id:
                            specie_id.pollen_transport_id = pollen_transport_id
                    if self.has_tongue:
                        tongue_id = self.get_or_create_element(tongue_name, tongue_model)
                        if tongue_id:
                            specie_id.tongue_id = tongue_id
                    if self.has_season:
                        season_id = self.get_or_create_element(season_name, season_model)
                        if season_id:
                            specie_id.season_id = season_id
                    if self.has_lecty:
                        lecty_id = self.get_or_create_element(lecty_name, lecty_model)
                        if lecty_id:
                            specie_id.lecty_id = lecty_id
                    if self.has_diet_breath:
                        diet_breath_id = self.get_or_create_element(diet_breath_name, diet_breath_model)
                        if diet_breath_id:
                            specie_id.diet_breath_id = diet_breath_id
                    if self.has_eu_iucn_status:
                        eu_iucn_status_id = self.get_or_create_element(eu_iucn_status_name, eu_iucn_status_model)
                        if eu_iucn_status_id:
                            specie_id.eu_iucn_status_id = eu_iucn_status_id
                    if self.has_be_iucn_status:
                        be_iucn_status_id = self.get_or_create_element(be_iucn_status_name, be_iucn_status_model)
                        if be_iucn_status_id:
                            specie_id.be_iucn_status_id = be_iucn_status_id
                    if self.has_introduced:
                        introduced_id = self.get_or_create_element(introduced_name, introduced_model)
                        if introduced_id:
                            specie_id.introduced_id = introduced_id
                    if self.has_comment:
                        if comment:
                            specie_id.comment = comment

        if self.has_sub_specie:
            if not specie_id:
                is_import_successful = False
                message += 'Specie required'
            else:
                sub_specie_id = self.get_or_create_element_with_parent(
                    specie_id, specie_field, sub_specie_name, sub_specie_model)
                if not sub_specie_id:
                    is_import_successful = False
                    message = 'Sub Specie'

        return is_import_successful, message

    def get_or_create_element(self, element_name, element_model):
        self.ensure_one()
        if not element_name:
            return False
        element_id = self.env[element_model].search([('name','=',element_name)])
        if not element_id:
            element_id = self.env[element_model].create({'name': element_name})
        return element_id

    def get_or_create_element_with_parent(self, parent_id, parent_field_name, 
    element_name, element_model):
        self.ensure_one()
        if not element_name:
            return False
        element_id = self.env[element_model].search([
            ('name','=',element_name),
            (parent_field_name,'=',parent_id.id)
        ])
        if not element_id:
            element_id = self.env[element_model].create({
                'name': element_name,
                parent_field_name: parent_id.id})
        return element_id