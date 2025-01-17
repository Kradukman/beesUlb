# -*- encoding: utf-8 -*-
{
    'name': 'plant_ulb',
    'version': '13.0',
    'description': """Manage plant""",

    'depends': [
        'base',
    ],
    'data': [
        # assets
        # models

        # fields
        # actions
        # reports

        # securityvehicles_brands
        'security/ir.model.access.csv',

        # views
        'views/plant.xml',
        'views/specie.xml',
        'views/genus.xml',
        'views/family.xml',
        'views/wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}