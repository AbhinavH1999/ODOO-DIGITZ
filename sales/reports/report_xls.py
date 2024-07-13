
import xlsxwriter
from odoo import models

class SalesReportXlsx(models.AbstractModel):
    _name = 'report.sales.report_sales_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print('lines',lines)
        border=workbook.add_format({'border':1})
        bold = workbook.add_format({'bold': True,'border':1})
        format1=workbook.add_format({'font_size':10,'align':'vcenter','bold':True})
        format2=workbook.add_format({'font_size':10,'align':'vcenter',})
        sheet=workbook.add_worksheet('Sales report')
        sheet.set_column(2,8, 15)
        sheet.write(2,2,'Sequence number',format1)
        sheet.write(2,3,lines.name,format2)
        sheet.write(4,2,'Bio',format1)
        if lines.bio:
            sheet.write(4,3,lines.bio,format2)
        sheet.write(6,2,'partner_id',format1)
        sheet.write(6,3,lines.partner_id.name,format2)
        sheet.write(4,7,'quatation_date',format1)
        sheet.write(4,8,lines.date_order,format2)
        sheet.write(6,7,'price list',format1)
        sheet.write(6,8,lines.pricelist_id.id,format2)
        sheet.write(8,7,'payment term',format1)
        sheet.write(8,8,lines.payment_term_id.name,format2)

        sheet.write(10,2,'order lines',border)
        # sheet.write(11,2,obj.order_line.name,format2
        sheet.write(11,2,'product varient',bold )
        # sheet.write(11,3,objs.product_id.name,format2)
        sheet.write(11,3,'product',bold )
        # sheet.write(11,4,objs.product_template_id.name,format2)
        sheet.write(11,4,'description',bold )
        # sheet.write(11,5,objs.name,format2)
        sheet.write(11, 5, 'quantity',bold )
        # sheet.write(11, 6, objs.product_uom_qty, format2)
        sheet.write(11, 6, 'unit price', bold )
        # sheet.write(11, 7, objs.price_unit, format2)
        sheet.write(11, 7, 'tax', bold )
        # sheet.write(11, 8, objs.tax_id.id, format2)
        sheet.write(11, 8, 'subtotal', bold )
        # sheet.write(11, 9, objs.price_subtotal, format2)

        row=12
        total=0
        for line in lines.order_line:
                sheet.write(row,2,line.product_id.name,border)
                sheet.write(row, 3, line.product_template_id.name,border)
                sheet.write(row, 4, line.name, border)
                sheet.write(row, 5, line.product_uom_qty, border)
                sheet.write(row, 6, line.price_unit, border)
                if line.tax_id.id:
                    sheet.write(row, 7, line.tax_id.id, border)
                sheet.write(row, 8, line.price_subtotal, border)
                row+=1

                total = total + line.price_subtotal
        sheet.write(row , 7,'Total ',bold )
        sheet.write(row, 8,total, border)


