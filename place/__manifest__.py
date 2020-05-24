# -*- encoding: utf-8 -*-
{
    'name': 'Places',
    'version': '13.0',
    'description': """Manage places""",

    'depends': [
        'base',
        'mail',
        'contacts',
    ],
    'data': [
        # assets
        # models

        # fields
        # actions
        # reports

        # security
        'security/ir.model.access.csv',
        # views
        'views/place_module.xml',
        'views/place.xml',
        'views/date_of_sampling.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}