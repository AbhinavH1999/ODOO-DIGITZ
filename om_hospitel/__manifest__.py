{
    'name':'hospital Management System',
    'author':'Abhinav',
    'website':'www.odoo.com',
    'summary':'Odoo 16 Devolopment',
    'depends': ['base', 'mail','product'],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/patient.xml',
        'data/sequence.xml',
        'views/doctors.xml',
        'views/menu.xml',
        'views/template.xml',

    ]
}