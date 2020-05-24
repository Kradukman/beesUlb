# -*- encoding: utf-8 -*-
{
    'name': 'project_ulb',
    'version': '13.0',
    'description': """Manage Project, extend project""",

    'depends': [
        'base',
        'contacts',
        'place',
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
        'views/project_ulb_module.xml',
        'views/project.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}