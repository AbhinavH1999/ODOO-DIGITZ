# -*- coding: utf-8 -*-
{
    'name': 'Dgz Delivery',
    'author': 'Digitz/Vishnu',
    'website': 'www.digitztech.com',
    'depends': ['sale', 'sale_management','mail','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'views/main.xml',
        'views/smart_button.xml',
        'views/search.xml',
        'views/incoterms.xml',
        'views/delivery_status.xml',
    ],
    'assets': {
   'web.assets_backend': [
       'dgz_delivery/static/src/js/dgz_delivery.js',
       'dgz_delivery/static/src/xml/dgz_delivery.xml',
   ],
},
}
