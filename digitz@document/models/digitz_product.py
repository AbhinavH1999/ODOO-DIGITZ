from odoo import fields, models,api
class DigitzProduct(models.Model):
    _name = "digitz.seconds"
    _description ="sales second"


    description=fields.Char(String="description")
    quantity=fields.Integer(String="quantity",default=1)
    unit_price=fields.Monetary(String="unit_price")
    product_id=fields.Many2one('product.product',string='product')
    sales_order_id=fields.Many2one('digitz.document',string='sales order id')
    subtotal= fields.Monetary(string='subtotal ', compute='_subtotal', store=True)
    currency_id = fields.Many2one(related='sales_order_id.currency_id', string='Currency', store=True)



    # Total = fields.Float(string='Total ', compute='_total',store=True)


    # @api.onchange('product_id')
    # def _product(self):
    #     if self.product_id:
    #         self.description=self.product_id.description_sale
    #         self.unit_price=self.product_id.list_price


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

