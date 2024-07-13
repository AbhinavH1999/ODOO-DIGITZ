from odoo import api, fields, models, _, Command


class WizardsSales(models.TransientModel):
    _name = "wizards.sales"

    order_line_ids=fields.One2many(comodel_name="sales.wizard",inverse_name="order_line") # table in wizard


    def action_test14(self):
        obj = self.env['sale.order'].browse(self.env.context.get('active_id'))
        list=[]
        for  rec in self.order_line_ids:
            list.append(rec.line_id)
        product=self.env['sale.order.line'].search([('order_id','=',obj.id),('id','not in',list)])
        product.unlink()
        list5=[]
        for line in obj.order_line:
            list5.append(line.id)
            print(line.id)
        for line in self.order_line_ids:
            if line.line_id not in list5:
                obj.update({
                    'order_line': [(0, 0, {
                                'product_id':line.product.id,
                                # 'product_template_id': line.product.id,
                                'name': line.description,
                                'product_uom_qty': line.quantity,
                    })],
                })
            if line.line_id:
                s=self.env['sale.order.line'].search([('id','=',line.line_id)],limit=1)
                s.update({
                    'name':line.description,
                    'product_template_id': line.product.id,
                    'product_id': line.product.id,
                    'product_uom_qty': line.quantity,
                })



class SalesWizard(models.TransientModel):
    _name ="sales.wizard"

    order_line=fields.Many2one("wizards.sales",string="order line")
    product=fields.Many2one("product.product",string="product")
    description=fields.Char(string="description",)          # name of fields in table in wizard
    quantity=fields.Integer(string="quantity")
    line_id=fields.Integer(string="id")


    @api.onchange('product')
    def _product(self):
        if self.product:
            self.description=self.product.name





