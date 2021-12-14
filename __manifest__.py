# -*- coding: utf-8 -*-
{
    'name': "Topnet",

    'summary': """Gestion des dossiers clients PRO""",

    'description': """ """,

    'author': "GHARBI Rima",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': '-100',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'board', 'website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/fiche_client.xml',
        'views/agence.xml',
        'views/agent.xml',
        'views/dossier.xml',
        'views/abonnement.xml',
        'views/rdv.xml',
        'views/dashboard.xml',
        'views/website.xml',
        # 'views/user.xml',
        # 'views/website_menu.xml',

    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
