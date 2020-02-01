# -*- encoding: utf-8 -*-
{
    'name': 'insect_sample_ulb',
    'version': '13.0',
    'description': """Manage insect sample""",

    'depends': [
        'base',
        'insect',
        'place',
        'plant',
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
        'views/insect_sample.xml',
        'views/sample.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}