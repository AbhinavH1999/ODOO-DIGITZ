from odoo import api, fields, models, _, Command


class CancelWizards(models.TransientModel):
    _name = "cancel.wizards"



    order_line_ids = fields.One2many('wizards.cancel','order_id',)
    Total = fields.Float(string='Total ', compute='_total')

    # def action_test5(self):
    #     sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
        # print(sale_order.id)
        # sale_order_product_ids = self.env['sale.order.line'].search([('order_id', '=', sale_order.id)]).mapped(
        #     'product_id.id')
        # print(sale_order_product_ids)
        #
        # sale_order_product_ids = sale_order.order_line.mapped('product_id.id')#sale_order
        # print(sale_order_product_ids)
        # wizard_product_ids = sale_order.order_line.mapped('order_id')
        # print(wizard_product_ids)
        # # wizard_product_ids = [line.product.id for line in self.order_line_ids]
        # x=self.env['sale.order.line'].search([('order_id', '=', sale_order.id)])
        # sale_order_product_ids = self.env['sale.order.line'].search([('order_id', '=', sale_order.id)]).mapped(
        #     'product_id.id')

        # print(sale_order_product_ids)

        # for line in x:
        #     if line not in wizard_product_ids:
        #         print(x)
        #     # x.unlink()

        # return True


        # for line in sale_order.order_line:
        #     if line.product_id.id not in wizard_product_ids:
        #         print(line.product_id.id)
        #         # line.unlink()

        # return True
    def action_test5(self):
        obj = self.env['sale.order'].browse(self.env.context.get('active_id'))
        list4=[]
        for rec in self.order_line_ids:
            list4.append(rec.line_id)
        product = self.env['sale.order.line'].search([('order_id','=',obj.id),('id','not in',list4)])
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
                                'name': line.description,
                                'product_uom_qty': line.qty,
                                'price_unit': line.unit_price,
                                'tax_id': [(6, 0,line.tax.ids)],
                                'price_subtotal': line.subtotal,
                    })],
                })
            if line.line_id:
                s=self.env['sale.order.line'].search([('id','=',line.line_id)],limit=1)
                s.update({
                    'name':line.description,
                    'product_template_id': line.product.id,
                    'product_uom_qty': line.qty,
                    'price_unit': line.unit_price,
                    'tax_id': [(6, 0, line.tax.ids)],
                    'price_subtotal': line.subtotal
                })

    @api.depends('order_line_ids')
    def _total(self):
        total=0
        for rec in self.order_line_ids:
            total= total + rec.subtotal
        self.Total=total
        # print(self.Total)

    def action_test6(self):
        print('excel report')



class WizardsCancel(models.TransientModel):
    _name = "wizards.cancel"


    order_id = fields.Many2one('cancel.wizards', string='Sale Order',ondelete='cascade')

    product = fields.Many2one('product.product',string="product")
    description = fields.Char(string="description" ,readonly=False)
    qty = fields.Integer(string="qty",default=1)
    unit_price = fields.Float(string="unit_price")
    # tax = fields.Char(string="tax")
    tax = fields.Many2many( 'account.tax',string='tax')
    subtotal= fields.Float(string='subtotal' ,compute='_subtotal')
    line_id=fields.Integer(string='id')

    #
    # @api.onchange('name')
    # def name_(self):
        # print("name_ working ")
        # active_id=self._context.get('active_id')    #wizard values passed into your models in using activei d
        # if active_id:
        #     sale=self.env['sale.order'].browse(active_id)
        #     sale.update({'bio':self.name})

    @api.onchange('product')
    def _product(self):
        if self.product:
            self.description=self.product.name
            self.unit_price= self.product.list_price
            # self.tax = self.tax_id.id
            # self.tax=0

    @api.depends('unit_price','qty')
    def _subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price


    # @api.model_create_multi
    # def unlink(self):
    #     res=super(WizardsCancel,self).unlink()
    #     for record in self:
    #         record.order_line_ids.unlink()
    #     return res

        # return {
        #     'name': _('sales.order'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'cancel.wizards',
        #     'view_mode': 'tree',
        #     'domain': [('id', 'in', self.name.id)],
        # }

        #
        # for rec in self.env['sale.order'].search([]):
        #     rec.bio=rec.name
    #
    # class CrmWizard(models.TransientModel):
    #     _name = "crm.wizards"
    #     organization=fields.Char(string="organization")
    #     oppertunity=fields.Char(string="oppertunity")
    #     email = fields.Char(string="Email")
    #     phone= fields.Integer(string="Phone")
    #
    #     def action_test8(self):
    #         opportunity_obj = self.env['crm.lead'].browse(self.oppertunity.id)
    #         if opportunity_obj.exists():
    #             opportunity_obj.action_set_won_rainbowman()
    #
    #         return super(SaleOrder, self).action_test8()


    # class CrmWizard(models.TransientModel):
    #     _name = "crm.wizards"
    #
    #     organization = fields.Char(string="Organization")
    #     opportunity = fields.Char(string="Opportunity")
    #     email = fields.Char(string="Email")
    #     phone = fields.Char(string="Phone")
    #
    #     def action_test8(self):
    #         opportunity_obj = self.env['crm.lead'].search([('name', '=', self.opportunity)])
    #         print(opportunity_obj)
    #
    #         if opportunity_obj:
    #             opportunity_obj.action_set_won_rainbowman()
    #
    #         return {'type': 'ir.actions.act_window_close'}




class CrmWizard(models.TransientModel):
    _name = "crm.wizards"

    partner_id=fields.Many2one('res.partner',string='Organization')
    opportunity = fields.Char(string="Opportunity")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    def action_test8(self):
        # Active_id=self.env.context.get('active_id')
        # if Active_id:
        #     sale=self.env['sale.order'].browse(Active_id)
        #     opertunity=sale.opportunity_id
        #     print(opertunity.name)
        #
        #     if opertunity:
        #         opertunity.update({
        #             'partner_id':self.partner_id.id,
        #             'name': self.opportunity,
        #             'email_from': self.email,
        #             'phone': self.phone,
        #         })
        #     else:
        #         opertunity=self.env['crm.lead'].create({
        #             'partner_id':self.partner_id.id,
        #             'name': self.opportunity,
        #             'email_from': self.email,
        #             'phone': self.phone,
        #
        #         })
        #         sale.opportunity_id=opertunity.id


            # op=sale.opportunity_id.name     # crm  link in opertunity name in sale.order
            # print(op)
        self.env['crm.lead'].create({
            'partner_id': self.partner_id.id,
            'name': self.opportunity,
            'email_from': self.email,
            'phone': self.phone,

        })

    @api.onchange('partner_id')
    def partner(self):
        if self.partner_id:
            self.opportunity = self.partner_id.name
            self.email = self.partner_id.email
            self.phone = self.partner_id.phone









