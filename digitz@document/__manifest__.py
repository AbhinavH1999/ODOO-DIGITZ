{
    'name':'digitz@document',
    'author':'Abhinav',
    'website':'www.odoo.com',
    'summary':'Odoo 16 Devolopment',
    'depends': ['base', 'mail','product','sale_management','spreadsheet_dashboard'],
    'data':[
        'security/ir.models.access.csv',
        'data/sequence.xml',
        'reports/report.xml',
        'reports/digitz_pdf.xml',
        'views/digitz.xml',
        'views/menu.xml',
    ]
}