# -*- encoding: utf-8 -*-
{
    'name': 'insect_sample_ulb',
    'version': '13.0',
    'description': """Manage insect sample""",

    'depends': [
        'base',
        'mail',
        'contacts',
        'insect',
        'place',
        'plant',
        'project_ulb',
    ],
    'data': [
        # assets
        # models

        # fields
        # actions
        # reports
        'reports/sticker.xml',
        # securityvehicles_brands
        'security/ir.model.access.csv',

        # views
        'views/insect_sample.xml',
        'views/sample.xml',
        'views/wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}