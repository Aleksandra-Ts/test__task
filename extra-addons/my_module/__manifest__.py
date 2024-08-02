{
    'name': 'My Custom Module',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Tselovalnikova A.T.',
    'summary': 'A test task for Odoo 17',
    'description': 'This module adds a custom application to the Odoo menu.',
    'depends': ['base', 'mail'],
    'data': [
        'views/my_new_entity_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}