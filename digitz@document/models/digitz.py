# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from datetime import datetime
class DigitzDocument(models.Model):
    _name = "digitz.document"
    _description="digitz Records"

    ref = fields.Char(string="Reference", required=True ,readonly=True,default=lambda self: _('New'))
    name_id = fields.Many2one('res.partner', string="Name")
    email=fields.Char(string="email",required=True,)
    date=fields.Date(string='Date',default=datetime.today())
    Customer_ids = fields.One2many('digitz.seconds', 'sales_order_id', string='Customer info')
    source_id=fields.Many2one('sale.order', string="Source")
    attachment_ids = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel',
                                      'rental_id', 'attachment_id', string="Attachments",
                                      help="Images of the vehicle before contract/any attachments")
    command = fields.Html(string="Command")
    Estimate_value=fields.Float(string="Estimate value",compute='estimate',store=True)
    Total = fields.Float(string='Total ', compute='_total', store=True)
    currency_id = fields.Many2one(comodel_name='res.currency',required=True)
    # price = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('closed', 'Closed'),
    ], default="draft", string="Status", store=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")




    @api.depends('Customer_ids.subtotal')
    # def _total(self):
    #     total = 0
    #     for rec in self.Customer_ids.subtotal:
    #         total = total + rec.subtotal
    #     self.Total = total
    #     print(self.Total)
    def _total(self):
        for record in self:
            total = sum(record.Customer_ids.mapped('subtotal'))
            record.Total = total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            seq = self.env['ir.sequence'].next_by_code('digitz.document')
            print(seq,'ubytgvbty')
            vals['ref'] = seq
        return super(DigitzDocument, self).create(vals_list)

    @api.onchange('name_id')
    def _email(self):
        if self.name_id:
            self.email = self.name_id.email




    def new_(self):
        for rec in self:
            rec.state='draft'
    def processing(self):
        for rec in self:
            rec.state = 'ready'

    def Completed(self):
        for rec in self:
            rec.state = 'closed'





    # @api.onchange('source_id')
    # def _email(self):
    #     if self.source_id:
    #         self.email = self.source_id.partner_id.email


    @api.onchange('source_id')
    def source_(self):
        # if self.source_id:
        #     sale_order=self.source_id
        #     # self.Customer_ids=[(5,0,0)]
        #     for order_line in sale_order.order_line:
        #         self.Customer_ids=[(0,0,{
        #             'product_id':order_line.product_template_id.id,
        #             # 'unit_price':order_line.product_template_id.list_price,
        #             # 'description': order_line.product_template_id.description_sale,
        #             # 'description': order_line.product_id.description_sale,
        #
        #         })]
        #         print(order_line.product_id)

        if self.source_id:
            if self.source_id:
                sale_order = self.source_id
                self.Customer_ids.unlink()  # Clear existing lines
                lines = []
                for order_line in sale_order.order_line:
                    lines.append((0, 0, {
                        'product_id': order_line.product_id.id,
                        'description': order_line.product_id.description_sale,
                        # 'quantity': order_line.product_id.product_uom_qty,
                        'unit_price':order_line.product_id.list_price
                    }))
                self.Customer_ids = lines

    @api.depends('Customer_ids.subtotal')
    def estimate(self):
        for record in self:
            estimated = sum(record.Customer_ids.mapped('subtotal'))
            record.Estimate_value = estimated











