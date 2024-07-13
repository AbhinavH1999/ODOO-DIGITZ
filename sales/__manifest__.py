{
    'name':'_sales_inheritance',
    'author':'Abhinav',
    'website':'www.odoo.com',
    'summary':'Odoo 16 Devolopment',
     'depends':['sale','sale_crm','report_xlsx','crm'],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizards/crm.xml',
        'wizards/cancel.xml',
        'views/sale_inheritence.xml',
        # 'views/access.xml',
        'views/delivery.xml',
        # 'data/mail_template.xml',
        'views/menu.xml',
        # 'reports/report.xml',
        # 'reports/sales_quotation.xml',

    ]
}

