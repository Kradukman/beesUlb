from odoo import api, fields, models, _
import csv
import io
import base64


class InsectSuperFamily(models.Model):
    _name = "insect.super.family"
    _description = "Insect Super Family"

    name = fields.Char('Name', required=True)


class InsectSuperFamilyImportWizard(models.TransientModel):
    _name = 'insect.super.family.import.wizard'
    _description = 'Insect super family import wizard'

    csv_file = fields.Binary('csv file to import', required=True)
    start_line = fields.Integer('Start line', default=2, required=True)
    super_family_col = fields.Integer('Super Family Name column number', required=True)
    separator = fields.Char('Separator', default=',', required=True)

    def action_import(self):
        self.ensure_one()
        unimported_lines = []
        i = 1
        with io.BytesIO(base64.b64decode(self.csv_file)) as f:
            for line in f.getvalue().splitlines():
                if i >= self.start_line:
                    if len(line) > 0:
                        split = line.split(self.separator.encode())
                        super_family_id = self.get_or_create_super_family(split[self.super_family_col - 1].decode('utf-8'))
                        if not super_family_id:
                            unimported_lines.append('line % : %' %(i, line))
                i = i + 1
        if not unimported_lines:
            message = 'All lines imported successfully'
        else:
            message = ('unimported lines: %s' % message for message in unimported_lines)
        notification = {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Warning!'),
            'message': message,
            'sticky': False,
        }}
        return notification

    def get_or_create_super_family(self, name):
        self.ensure_one()
        super_family_id = self.env['insect.super.family'].search([('name','=',name)])
        if not super_family_id:
            super_family_id = self.env['insect.super.family'].create({'name': name})
        return super_family_id