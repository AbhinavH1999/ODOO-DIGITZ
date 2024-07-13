from odoo import fields, models,api
class SalesOrder(models.Model):
    _name = "sales.second"
    _description ="sales second"


    description=fields.Char(String="description")
    quantity=fields.Integer(String="quantity",default=1)
    unit_price=fields.Float(String="unit_price")
    product_id=fields.Many2one('product.template',string='product')
    sales_order_id=fields.Many2one('sale.order',string='sales order id')
    subtotal= fields.Float(string='subtotal ', compute='_subtotal', store=True)
    # Total = fields.Float(string='Total ', compute='_total',store=True)


    @api.onchange('product_id')
    def _product(self):
        if self.product_id:
            self.description=self.product_id.description_sale
            self.unit_price=self.product_id.list_price


    @api.depends('unit_price','quantity')
    def _subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price



    # @api.depends('subtotal')
    # def _total(self):
    #     for order in self:
    #         order.Total =sum(self.product_id.mapped('subtotal'))
    #         print(order.Total)

    # @api.depends('subtotal')
    # def _total(self):
    #     total = 0
    #      for rec in self:
    #         total = total + rec.subtotal
    #         rec.Total = total
    #     print(rec.Total)