# -*- encoding: utf-8 -*-
{
    'name': 'insect_ulb',
    'version': '13.0',
    'description': """Manage insect""",

    'depends': [
        'base',
        'mail',
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
        'views/sub_specie.xml',
        'views/genus.xml',
        'views/family.xml',
        'views/super_family.xml',
        'views/sub_family.xml',
        'views/tribe.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}