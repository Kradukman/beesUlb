# -*- encoding: utf-8 -*-
{
    'name': 'trap_ulb',
    'version': '13.0',
    'description': """Manage trap""",

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
        'views/trap_module.xml',
        'views/trap.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}