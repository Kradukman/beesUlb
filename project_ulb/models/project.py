from odoo import api, fields, models, _


class ULBProject(models.Model):
    _name = 'project_ulb.project'

    name = fields.Char('Project', required=True)
    year = fields.Integer('Year', required=True, default=2019)
    site_ids = fields.Many2many('place.place', string='Sites')
    leader_ids = fields.Many2many('res.partner', string='Leader', required=True)


class PlacePlace(models.Model):
    _inherit = "place.place"
    _description = "Place Place"

    project_ids = fields.Many2many(comodel_name='project_ulb.project')