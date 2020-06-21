from odoo import api, fields, models, _
import csv
import io
import base64


class ImportWizard(models.TransientModel):
    _name = 'plant.import.wizard'
    _description = 'Import wizard'

    csv_file = fields.Binary('csv file to import', required=True)
    start_line = fields.Integer('Start line', default=2, required=True)
    separator = fields.Char('Separator', default=',', required=True)
    error_message = fields.Text('Message', readonly=True)
    # Plant
    has_family = fields.Boolean('Family', default=False)
    family_col = fields.Integer('Family column number')
    has_genus = fields.Boolean('Genus', default=False)
    genus_col = fields.Integer('Genus column number')
    has_specie = fields.Boolean('Specie', default=False)
    specie_col = fields.Integer('Specie column number')

    # Plant onchange
    @api.onchange('has_family')
    def onchange_family(self):
        if not self.has_family:
            self.has_genus = False
            self.onchange_genus

    @api.onchange('has_genus')
    def onchange_genus(self):
        if self.has_genus:
            self.has_family = True
            self.onchange_family()
        else:
            self.has_specie = False
            self.onchange_specie

    @api.onchange('has_specie')
    def onchange_specie(self):
        if self.has_specie:
            self.has_genus = True
            self.onchange_genus()

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
        # plant init
        family_id = False
        family_model = 'plant.family'
        family_field = 'family_id'
        genus_id = False
        genus_model = 'plant.genus'
        genus_field = 'genus_id'
        specie_id = False
        specie_model = 'plant.specie'
        specie_field = 'specie_id'

        # PREPROCESS
        # Plant
        if self.has_family:
            family_name = split[self.family_col - 1].decode('utf-8')
        if self.has_genus:
            genus_name = split[self.genus_col - 1].decode('utf-8')
        if self.has_specie:
            specie_name = split[self.specie_col - 1].decode('utf-8')

        # IMPORT
        # import plant
        if self.has_family:
            family_id = self.get_or_create_element(family_name, family_model)
            if not family_id:
                is_import_successful = False
                message = 'plant family error'
        
        if self.has_genus:
            if not family_id:
                is_import_successful = False
                message += 'Plant family required'
            else:
                genus_id = self.get_or_create_element_with_parent(
                    family_id, family_field, genus_name, genus_model)
                if not genus_id:
                    is_import_successful = False
                    message = 'Plant genus'

        if self.has_specie:
            if not genus_id:
                is_import_successful = False
                message += 'Plant genus required'
            else:
                specie_id = self.get_or_create_element_with_parent(
                    genus_id, genus_field, specie_name, specie_model)
                if not specie_id:
                    is_import_successful = False
                    message = 'Plant Specie'

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