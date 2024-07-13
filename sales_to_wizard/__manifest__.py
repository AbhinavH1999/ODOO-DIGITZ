{
    'name':'_sales_to_wizard',
    'author':'Abhinav',
    'website':'www.odoo.com',
    'summary':'Odoo 16 Devolopment',
     'depends':['sale','base','product'],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/saleswizard.xml',
        'wizard/wizard.xml'



    ]
}