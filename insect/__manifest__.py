# -*- encoding: utf-8 -*-
{
    'name': 'insect_ulb',
    'version': '13.0',
    'description': """Manage insect""",

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
        'views/insect.xml',
        'views/specie.xml',
        'views/genus.xml',
        'views/family.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}