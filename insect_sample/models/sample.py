from odoo import api, fields, models, _
from odoo.exceptions import Warning
import csv
import io
import base64

STATE_SELECTION = [('draft', 'Draft'), ('validated', 'Validated')]

class InsectSex(models.Model):
    _name = 'insect.sample.sex'
    _description = 'Insect Sample Sex'

    name = fields.Char('Insect sex')


class InsectTrap(models.Model):
    _name = 'insect.sample.trap'
    _description = 'Insect Sample Trap'

    name = fields.Char('Name', required=True)


class InsectPhysicalStatus(models.Model):
    _name = 'insect.sample.physical.status'
    _description = "Insect Sample Physical status"

    name = fields.Char('Name', required=True)


class InsectCollectionStatus(models.Model):
    _name = "insect.sample.collection.status"
    _description = "Insect Sample Collection status"

    name = fields.Char('Name', required=True)


class InsectSample(models.Model):
    _name = "insect.sample.sample"
    _description = "Insect Sample"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # TODO add automatic sequence on name 
    name = fields.Char('Insect Sample Name', compute='_compute_name', store=True)
    legacy_name = fields.Char('Insect legacy name', default=False)
    # INSECT
    specie_id = fields.Many2one('insect.specie', string='Specie', copy=True)
    genus_id = fields.Many2one('insect.genus', related='specie_id.genus_id', string='Genus', readonly=True, copy=True)
    subspecie_id = fields.Many2one('insect.subspecie', string='Subspecie', copy=True)
    
    # PLACE
    place_id = fields.Many2one('place.place', required=True, copy=True)
    country_id = fields.Many2one('res.country', related='place_id.country_id', readonly=True, copy=True)
    state_id = fields.Many2one('res.country.state', related='place_id.state_id', readonly=True, copy=True)
    city_id = fields.Many2one('place.city', related='place_id.city_id', readonly=True, copy=True)

    # PLANT
    plant_id = fields.Many2one('plant.specie', string='Plant specie', copy=True)
    plant_genus_id = fields.Many2one('plant.genus', related='plant_id.genus_id', string='Plant genus', readonly=True, copy=True)
    plant_family_id = fields.Many2one('plant.family', related='plant_id.family_id', string='Plant family', readonly=True, copy=True)

    # PROJECT
    project_id = fields.Many2one('project_ulb.project', string='Project', required=True, copy=True)
    year = fields.Integer('Year', related='project_id.year', readonly=True)
    project_leader_ids = fields.Many2many('res.partner', string='Project leader', related='project_id.leader_ids', readonly=True)

    # SAMPLE
    identifier_id = fields.Many2one('res.partner', string='Identifier', copy=True)
    sex_id = fields.Many2one('insect.sample.sex', string='Sex', copy=True)
    trap_id = fields.Many2one('insect.sample.trap', string='Trap', required=True, copy=True)
    physical_status_id = fields.Many2one('insect.sample.physical.status', string='Physical Status', required=True, copy=True)
    collection_status_id = fields.Many2one('insect.sample.collection.status', string='Collection Status', copy=True)
    sampling_date = fields.Date('Sampling Date', required=True, copy=True) # Use domain to filter on view

    remark = fields.Char('Remark')

    state = fields.Selection(
        STATE_SELECTION, 
        string='Status', groups='base.group_erp_manager',
        default='draft', tracking=True)
    sampler_id = fields.Many2one('res.partner', string='Sampler', 
        default=lambda self: self.env.user.partner_id, required=True)

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

    def duplicate_sample(self, number_duplicate):
        self.ensure_one()
        for i in range(0, number_duplicate):
            self.copy()

    def open_duplicate_wizard(self):
        self.ensure_one()
        return {
            'name': 'duplicate_wizard',
            'view_mode': 'form',
            'res_model': 'insect.sample.duplicate.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'id': self.id},
        }


class InsectSampleDuplicateWizard(models.TransientModel):
    _name = 'insect.sample.duplicate.wizard'
    _description = 'Duplicate wizard'

    duplicate_number = fields.Integer('Duplication')

    def duplicate_sample(self):
        self.ensure_one()
        if self.duplicate_number < 1:
            raise Warning('Duplicate number less than 0')
        sample_id = self.env.context.get('id')
        sample = self.env['insect.sample.sample'].search([('id','=', sample_id)])
        sample.duplicate_sample(self.duplicate_number)

class InsectSampleImportWizard(models.TransientModel):
    _name = "insect.sample.import.wizard"
    _description = 'Insect sample import wizard'

    csv_file = fields.Binary('csv file to import')
    start_line = fields.Integer('Start line', default=2)
    separator = fields.Char('Separator', default=',', required=True)
    error_message = fields.Text('Message', readonly=True)

    # Mandatory fields
    place_name_col = fields.Integer('Place name column number', default=12)
    project_name_col = fields.Integer('Project name column number', default=2)
    trap_name_col = fields.Integer('Trap column number', default=14)
    physical_status_name_col = fields.Integer('Physical status column number', default=15)
    sampling_date_col = fields.Integer('Sampling date column number', default=19)
    sampler_name_col = fields.Integer('Sampler name column number', default=13)

    # Not mandatory fields
    state_col = fields.Integer('Status column number', default=17)
    has_state = fields.Boolean('Has status', default=False)
    identifier_name_col = fields.Integer('Identifier name column number', default=5)
    has_identifier_name = fields.Boolean('Has identifier', default=False)
    genus_name_col = fields.Integer('Genus name column number', default=8)
    has_genus_name = fields.Boolean('Has Genus', default=False)
    specie_name_col = fields.Integer('Species name column number', default=9)
    has_specie_name = fields.Boolean('Has specie', default=False)
    subspecie_name_col = fields.Integer('Subspecies name column number', default=10)
    has_subspecie_name = fields.Boolean('Has subspecie', default=False)
    sex_col = fields.Integer('Sex column number', default=11)
    has_sex = fields.Boolean('Has sex', default=False)
    collection_status_name_col = fields.Integer('Collection status column number', default=16)
    has_collection_status_name = fields.Boolean('Has collection', default=False)
    remark_col = fields.Integer('Remark column number', default=18)
    has_remark = fields.Boolean('Has remark', default=False)
    legacy_name_col = fields.Integer('Legacy column number', default=1)
    has_legacy_name = fields.Boolean('Has legacy', default=False)
    state_possible_value = fields.Char('Status possible values', compute='_compute_state_value', readonly=True)

    @api.onchange('has_state')
    def _compute_state_value(self):
        self.ensure_one()
        for val in dict(STATE_SELECTION).keys():
            if not self.state_possible_value:
                self.state_possible_value = '%s' % (val)
            else:
                self.state_possible_value = '%s - %s' % (self.state_possible_value, val)

    @api.onchange('has_genus_name')
    def onchange_has_genus_name(self):
        if self.has_genus_name:
            self.has_specie_name = True
        else:
            self.has_specie_name = False
    
    @api.onchange('has_specie_name')
    def onchange_has_specie_name(self):
        if self.has_specie_name:
            self.has_genus_name = True
        else:
            self.has_genus_name = False

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
        # Mandatory fields

        place_name = split[self.place_name_col - 1].decode('utf-8')
        place_model = 'place.place'
        project_name = split[self.project_name_col - 1].decode('utf-8')
        project_model = 'project_ulb.project'
        trap_name = split[self.trap_name_col - 1].decode('utf-8')
        trap_model = 'insect.sample.trap'
        physical_status_name = split[self.physical_status_name_col - 1].decode('utf-8')
        physical_status_model = 'insect.sample.physical.status'
        
        sampling_date = split[self.sampling_date_col - 1].decode('utf-8')
        sampler_name = split[self.sampler_name_col - 1].decode('utf-8')
        sampler_model = 'res.partner'

        # Check if mandatory fields are not empty
        if not place_name:
            is_import_successful = False
            message = 'Place empty'
        if not project_name:
            is_import_successful = False
            message = 'Project empty'
        if not trap_name:
            is_import_successful = False
            message = 'Trap empty'
        if not physical_status_name:
            is_import_successful = False
            message = 'Physical status empty'
        if not sampling_date:
            is_import_successful = False
            message = 'Sampling date empty'
        if not sampler_name:
            is_import_successful = False
            message = 'Sampler empty'

        if is_import_successful:
            place_id = self.get_element(place_name, place_model)
            project_id = self.get_element(project_name, project_model)
            trap_id = self.get_element(trap_name, trap_model)
            physical_status_id = self.get_element(physical_status_name, physical_status_model)
            sampler_id = self.get_element(sampler_name, sampler_model)
            if not place_id:
                is_import_successful = False
                message = 'Place not found empty'
            if not project_id:
                is_import_successful = False
                message = 'Project not found empty'
            if not trap_id:
                is_import_successful = False
                message = 'Trap not found empty'
            if not physical_status_id:
                is_import_successful = False
                message = 'Physical status not found empty'
            if not sampler_id:
                is_import_successful = False
                message = 'Sampler not found empty'
            sample_id = self.env['insect.sample.sample'].create({
                'place_id': place_id.id,
                'project_id': project_id.id,
                'trap_id': trap_id.id,
                'physical_status_id': physical_status_id.id,
                'sampler_id': sampler_id.id,
                'sampling_date': sampling_date
                })
            if not sample_id:
                is_import_successful = False
                message = 'Sample not created error'
            else:
                genus_id = False
                specie_id = False
                subspecie_id = False
                if self.has_state:
                    state = split[self.state_col - 1].decode('utf-8')
                    if state in dict(STATE_SELECTION).keys():
                        sample_id.state = state
                if self.has_identifier_name:
                    identifier_name = split[self.identifier_name_col - 1].decode('utf-8')
                    if identifier_name and identifier_name != '':
                        identifier_id = self.get_element(identifier_name, 'res.partner')
                        if identifier_id:
                            sample_id.identifier_id = identifier_id
                if self.has_genus_name:
                    genus_name = split[self.genus_name_col - 1].decode('utf-8')
                    if genus_name and genus_name != '':
                        genus_id = self.get_element(genus_name, 'insect.genus')
                        if genus_id:
                            sample_id.genus_id = genus_id
                if self.has_specie_name:
                    specie_name = split[self.specie_name_col - 1].decode('utf-8')
                    if genus_id and specie_name and specie_name != '':
                        specie_id = self.get_element_with_parent(genus_id, 'genus_id',
                        specie_name, 'insect.specie')
                        if specie_id:
                            sample_id.specie_id = specie_id
                if self.has_subspecie_name:
                    subspecie_name = split[self.subspecie_name_col - 1].decode('utf-8')
                    if specie_id and subspecie_name and subspecie_name != '':
                        subspecie_id = self.get_element_with_parent(specie_id, 'specie_id',
                        subspecie_name, 'insect.subspecie')
                        if subspecie_id:
                            sample_id.subspecie_id = subspecie_id
                if self.has_sex:
                    sex = split[self.sex_col - 1].decode('utf-8')
                    if sex and sex != '':
                        sex_id = self.get_element(sex, 'insect.sample.sex')
                        if sex_id:
                            sample_id.sex_id = sex_id
                if self.has_collection_status_name:
                    collection_status_name = split[self.collection_status_name_col - 1].decode('utf-8')
                    if collection_status_name and collection_status_name != '':
                        collection_status_id = self.get_element(collection_status_name, 
                        'insect.sample.collection.status')
                        if collection_status_id:
                            sample_id.collection_status_id = collection_status_id
                if self.has_remark:
                    remark = split[self.remark_col - 1].decode('utf-8')
                    if remark and remark != '':
                        sample_id.remark = remark
                if self.has_legacy_name:
                    legacy_name = split[self.legacy_name_col - 1].decode('utf-8')
                    if legacy_name and legacy_name != '':
                        sample_id.legacy_name = legacy_name

                # state_col
                # identifier_name_col
                # genus_name_col
                # specie_name_col
                # subspecie_name_col
                # sex_col
                # collection_status_name_col
                # remark_col
                # legacy_name_col
        return is_import_successful, message

    def get_element(self, element_name, element_model):
        self.ensure_one()
        if not element_name:
            return False
        element_id = self.env[element_model].search([('name','=',element_name)])
        return element_id

    def get_element_with_parent(self, parent_id, parent_field_name, 
    element_name, element_model):
        self.ensure_one()
        if not element_name:
            return False
        element_id = self.env[element_model].search([
            ('name','=',element_name),
            (parent_field_name,'=',parent_id.id)
        ])
        return element_id