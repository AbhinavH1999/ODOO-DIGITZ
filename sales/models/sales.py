from odoo import fields, models,api
from colorama import Fore
class SalesInheritence(models.Model):
    _inherit = 'sale.order'
    bio=fields.Char(String='bio')
    Customer_ids= fields.One2many('sales.second', 'sales_order_id', string='Customer info')
    Total = fields.Float(string='Total ', compute='_total')
    # order_id = fields.Many2one('sale.order', string='Sale Order')
    delivery_count = fields.Integer(string='Delivery Orders')
    @api.depends('Customer_ids')
    def _total(self):
        total=0
        for rec in self.Customer_ids:
            total= total + rec.subtotal
        self.Total=total
        print(self.Total)
        print(Fore.GREEN)


    # def action_test2(self):
        # action=self.env.ref('sales.cancel_wizard').read()[0]
        # return action
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'cancel.wizards',
        #     'view_mode': 'form',
        #     'target':'new'
        #
        #     }

    def action_test2(self):
        list=[]
        for rec in self.order_line:
            print(rec.order_id)
            list.append({
                'product':rec.product_id.id,
                'description':rec.name,
                'qty':rec.product_uom_qty,
                'unit_price':rec.price_unit,
                'tax':rec.tax_id.ids,
                'subtotal':rec.price_subtotal,
                'line_id':rec.id
            })

        print(list)



        print(list)


        return{
                    'type':'ir.actions.act_window',
                    'res_model':'cancel.wizards',                      #APPEND TO WIZARD DISPLAY WIZARD
                    'view_mode': 'form',
                    'target':'new',
                    'context':{'default_order_line_ids':list}

                }

    def action_test7(self):

        return{
                    'type':'ir.actions.act_window',
                    'res_model':'crm.wizards',                      #APPEND TO WIZARD DISPLAY WIZARD
                    'view_mode': 'form',
                    'target':'new',

                }

    def action_confirm(self):
        res = super(SalesInheritence, self).action_confirm()
        template=self.env.ref('sales.confirmation_mail_template')
        for rec in self:
            rec.delivery_count = 1
            template.send_mail(rec.id)

        return res
    def action_cancel(self):
        res = super(SalesInheritence, self).action_cancel()
        for rec in self:
            rec.delivery_count = 0
        return res

    def action_test10(self):
        return{
                    'type':'ir.actions.act_window',
                    'res_model':'delivery.order',                      #APPEND TO WIZARD DISPLAY WIZARD
                    'view_mode': 'form',
                    'models':'ir.ui.view',
                    'target':'current',

                }




















