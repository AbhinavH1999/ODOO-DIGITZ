{
    'name':'systray_form',
    'author':'Abhinav',
    'website':'www.odoo.com',
    'summary':'Odoo 16 Devolopment',
     'depends':['base'],
      'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/systray_form.xml',
    ],
    'assets': {
    'web.assets_backend': [
       'systray_form/static/src/js/systray_forms.js',
       'systray_form/static/src/xml/systray_forms.xml',

        ],
        },

}
