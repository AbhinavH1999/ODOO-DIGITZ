from odoo import fields, models, api
from odoo.exceptions import AccessError,ValidationError


class SaleOrderSmartButton(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        for order in self.order_line:
            order.qty_delivered = 0
        search = self.env['sale.order.delivery'].sudo().search([('source_id', '=', self.id)])
        user = self.env.user
        if search:
            if not user.has_group('dgz_delivery.group_delivery_admin'):
                if search.create_uid.id != user.id and search.delivery_agent_id.id != user.id:
                    raise AccessError("You do not have sufficient access rights to cancel the associated delivery. Please contact your administrator.")
                search.state = 'draft'
        action = super(SaleOrderSmartButton, self).action_cancel()
        return (action)

    def action_confirm(self):
        commercial_line = []
        shipment_term = []
        res = self.env['sale.order.delivery'].sudo().search([('source_id', '=', self.id)])
        if not res:
            for order in self.order_line:
                order.qty_delivered = 0
                commercial_line.append((0, 0, {
                    'product_id': order.product_template_id.id,
                    'product_code': order.product_id.default_code,  # Use default_code from product_id
                    'demand': order.product_uom_qty,
                    'done': order.qty_delivered,
                    'sale_order_line_id': order.id,
                    'tax_ids': order.tax_id,
                    'price_unit': order.price_unit,
                }))
                if not order.product_template_id.detailed_type == 'service':
                    shipment_term.append((0, 0, {
                        'product_id': order.product_template_id.id,
                        'product_code': order.product_id.default_code,  # Use default_code from product_id
                    }))
            vals = {
                'partner_id': self.partner_id.id,
                'source_id': self.id,
                'commercial_line_ids': commercial_line,
                'shipment_line_ids': shipment_term,
                'ship_to': self.partner_id.state_id.name,
                'bill_customer_address_id': self.partner_id.id,

            }
            search = self.env['sale.order.delivery'].search([('source_id', '=', self.id)])
            if not search:
                self.env['sale.order.delivery'].create(vals)
            else:
                search.commercial_line_ids.unlink()
                search.shipment_line_ids.unlink()
                search.update(vals)
            action = super(SaleOrderSmartButton, self).action_confirm()
            return (action)
        else:
            action = super(SaleOrderSmartButton, self).action_confirm()
            return (action)

    def delivery_dgz(self):
        res = self.env['sale.order.delivery'].sudo().search([('source_id', '=', self.id)])
        if res.id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.delivery',
                'view_mode': 'form',
                'res_id': res.id,
            }
class FetchDataLine(models.Model):
    _name = "fetch.data.line"
    _description = "Fetch Data Line"

    product_code = fields.Char(string="Product Code")
    value = fields.Float(string="Value")
    fetch_data_id = fields.Many2one('sale.order.delivery', string="Fetch Data")
    product_id =  fields.Many2one('product.template', 'Product Name')
    shipment_mode = fields.Selection([('aw', 'AW'),('bl', 'BL')], 'Shipment mode')
    aw_bl_no = fields.Text(string="AW/BL No")
    aw_bl_date =fields.Date(string="AW/BL Date")
    etd = fields.Date(string="ETD")
    eta  = fields.Date(string="ETA")
    delivery_status = fields.Many2one("delivery.status", 'Delivery Status')


class SaleOrderDelivery(models.Model):
    _name = 'sale.order.delivery'
    _inherit = 'mail.thread'

    created_ids = fields.One2many('fetch.data.line', 'fetch_data_id', string="Fetch Data Lines")
    partner_id = fields.Many2one('res.partner', 'Customer', tracking=True)
    name = fields.Char(tracking=True, default=lambda self: ('New'))
    scheduled_date = fields.Datetime('Scheduled Date', tracking=True)
    source_id = fields.Many2one('sale.order', tracking=True)
    delivery_agent_id = fields.Many2one('res.users', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('ready', 'Ready'), ('done', 'Done'), ('cancel', 'Cancel')],
                             required=True, default='draft', tracking=True)
    commercial_line_ids = fields.One2many('commercial.delivery.product', 'commercial_id', 'Delivery Lines',
                                          tracking=True)
    shipment_line_ids = fields.One2many('shipment.delivery.terms', 'shipment_term_id', 'Shipment Lines',
                                          tracking=True)
    ship_from = fields.Char(string="From", tracking=True)
    ship_to = fields.Char(string="To", tracking=True)
    ship_marks = fields.Char(string="Shipping Marks", default="TESTRON GROUP", tracking=True)
    inco_price = fields.Float(string="Shipping Cost", tracking=True)
    inco_term_id = fields.Many2one('inco.terms', tracking=True)
    bill_customer_address_id = fields.Many2one('res.partner', string="Bill to", tracking=True)
    heading = fields.Selection([('TESTRON TRADING L.L.C', 'TESTRON TRADING L.L.C'), ('TESTRON CO. LTD', 'TESTRON CO. LTD')], string="Invoice Type")
    Ship_customer_address_id = fields.Many2one('res.partner', string="Ship to", tracking=True)
    head_line = fields.Char(string="Head Line", tracking=True)
    contact_person = fields.Many2one('res.partner', string="Contact Person", tracking=True)
    seller = fields.Char("Seller", tracking=True)
    currency_id = fields.Many2one('res.currency', related='source_id.pricelist_id.currency_id',
                                  string='Currency')
    received_by = fields.Char("Received By", tracking=True)
    signatured_by = fields.Binary("Signatured By", tracking=True)
    amount_untaxed = fields.Monetary(string="Untaxed Amount", compute='_compute_total')
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_total')
    total = fields.Monetary(string="Total", compute='_compute_total')

    def _post_line_changes_message(self, old_val):
        for delivery in self:
            if delivery.commercial_line_ids and delivery.shipment_line_ids:
                for line_id, old_values in old_val.items():
                    messages = []
                    if 'commercial_id' in old_values and old_values['commercial_id'].state != 'cancel':
                        line = delivery.commercial_line_ids.filtered(lambda x: x.id == line_id)
                        for field, old_value in old_values.items():
                            new_value = getattr(line, field)
                            display_name = line._fields[field].string
                            if field == 'product_id':
                                new_value = new_value.name
                            if old_value != new_value:
                                if old_value == False:
                                    old_value = 'None'
                                elif new_value == False:
                                    new_value = 'None'
                                message = f"<li>{old_value} <i class='o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600'></i> <span class='text-info fw-bold'>{new_value}</span><i>({display_name})</i></li>"
                                messages.append(message)
                        combined_message = ('\n').join(messages)
                        delivery.message_post(body=f"Commercial Invoice<br><ul>{combined_message}</ul>")

                    elif 'shipment_term_id' in old_values:
                        line_pack = delivery.shipment_line_ids.filtered(lambda x: x.id == line_id)
                        for field, old_value in old_values.items():
                            new_value = getattr(line_pack, field)
                            display_name = line_pack._fields[field].string
                            if field == 'product_id':
                                new_value = new_value.name
                            if old_value != new_value:
                                if old_value == False:
                                    old_value = 'None'
                                if new_value == False:
                                    new_value = 'None'
                                message = f"<li>{old_value} <i class='o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600'></i> <span class='text-info fw-bold'>{new_value}</span><i>({display_name})</i></li>"
                                messages.append(message)
                        combined_message = ('\n').join(messages)
                        delivery.message_post(body=f"Shipment terms<br><ul>{combined_message}</ul>")

    @api.depends('commercial_line_ids.tax_ids', 'commercial_line_ids.product_id', 'commercial_line_ids.demand')
    def _compute_total(self):
        total_count = 0
        tax = 0
        for price in self.commercial_line_ids:
            taxes = price.tax_ids.mapped('amount')
            tax_amount = sum(taxes) / 100 * price.price_subtotal if taxes else 0
            tax += tax_amount
            total_count += price.price_subtotal
        self.amount_untaxed = total_count
        self.amount_tax = tax
        self.total = total_count + tax

    def delivery_done(self):
        self.state = "done"
        if self.state == 'done':
            for products in self.commercial_line_ids:
                products.sale_order_line_id.sudo().write({'qty_delivered' : products.done})

    def delivery_cancel(self):
        self.state = "cancel"
        for qty in self.commercial_line_ids.sale_order_line_id:
            qty.sudo().write({'qty_delivered': 0})
        for products in self.commercial_line_ids:
            products.sudo().write({'done': 0})


    def delivery_ready(self):
        self.state = "ready"

    def delivery_draft(self):
        self.state = "draft"

    def redirect_sale(self):
        return {
            'name': 'order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.source_id.id,
        }

    @api.model_create_multi
    def create(self, record):
        for rec in record:
            rec['name'] = self.env['ir.sequence'].next_by_code('sale.order.delivery')
        result = super(SaleOrderDelivery, self).create(record)
        return result








class CommercialLines(models.Model):
    _name = "commercial.delivery.product"

    product_id = fields.Many2one('product.template', 'Product Name')
    product_code = fields.Char(string="Product Code")
    hs_code = fields.Char(string="HS Code")
    demand = fields.Float('Quantity', default=1)
    price_unit = fields.Float(string='Unit Price')
    price_subtotal = fields.Monetary(string='Subtotal', compute="_compute_subtotal")
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    currency_id = fields.Many2one('res.currency', related='commercial_id.source_id.pricelist_id.currency_id',
                                  string='Currency')
    done = fields.Float('Done')
    note = fields.Text('Note')
    commercial_id = fields.Many2one('sale.order.delivery', 'Delivery')
    sale_order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')

    def write(self, vals):
        old_values = {}
        for line in self:
            old_values[line.id] = {
                'product_id': line.product_id.name,
                'price_unit': line.price_unit,
                'product_code': line.product_code,
                'hs_code': line.hs_code,
                'demand': line.demand,
                'done': line.done,
                'note': line.note,
                'commercial_id':line.commercial_id
            }
        res = super(CommercialLines, self).write(vals)
        if not self.env.context.get('skip_post_line_changes_message'):
            self.commercial_id._post_line_changes_message(old_values)
        return res

    @api.constrains('product_id')
    def _constrains_pro_id(self):
        if not self.product_id or len(self.product_id) == 0:
            raise ValidationError("You must add at least one product!")

    @api.onchange('done')
    def onchange_done(self):
        if self.done > self.demand:
            self.done = self.demand

    @api.onchange('product_id')
    def onchange_prod_id(self):
        if self.price_unit:
            self.price_unit = self.product_id.list_price
            self.product_code = self.product_id.default_code

    @api.depends('tax_ids', 'product_id', 'demand', 'price_unit')
    def _compute_subtotal(self):
        for total in self:
            total.price_subtotal = total.demand * total.price_unit


class ShipmentTerms(models.Model):
    _name = "delivery.status"

    name = fields.Char('Status of delivery')
    is_done = fields.Boolean("Delivery Done")


class ShipmentTerms(models.Model):
    _name = "shipment.delivery.terms"

    product_id = fields.Many2one('product.template', 'Product Name')
    product_code = fields.Char(string="Product Code")
    shipment_mode = fields.Selection([('aw', 'AW'),('bl', 'BL')], 'Shipment mode')
    aw_bl_no = fields.Text(string="AW/BL No")
    aw_bl_date = fields.Date(string="AW/BL Date")
    etd = fields.Date(string="ETD")
    eta = fields.Date(string="ETA")
    delivery_status = fields.Many2one("delivery.status", 'Delivery Status')
    shipment_term_id = fields.Many2one('sale.order.delivery', 'Terms')
    done = fields.Boolean(string="green done",compute="green_decoration",defaulr=False)
    notify = fields.Boolean(string="notify", defaulr=False)
    form_id = fields.Integer()
    name=fields.Text(string="name")

    @api.onchange('done')
    def for_done_function(self):

        # k = self.env['sale.order.delivery'].browse(id)
        # print(self.form_id)
        data = []
        for record in self:
            if record.done:
                # print(record.form_id)
                data.append((0, 0, { 'product_code':record.product_code }))
                # print(data)
            delivery = self.env['sale.order.delivery'].search([('id', '=',record.form_id)])
            # print(delivery)
            delivery.created_ids = data


    @api.depends('delivery_status.is_done')
    def green_decoration(self):
        for record in self:
            record.done = record.delivery_status.is_done if record.delivery_status else False

    @api.model
    def create(self, vals):
        # Print creation values


        record = super(ShipmentTerms, self).create(vals)

        if record.done:
            record.write({'notify': True})




        # Format data for FetchData
            data = {
                'product_name': record.product_id.name if record.product_id else '',
                'product_code': record.product_code,
                'shipment_mode': record.shipment_mode,
                'aw_bl_no': record.aw_bl_no,
                'aw_bl_date': record.aw_bl_date,
                'etd': record.etd,
                'eta': record.eta,
                'delivery_status': record.delivery_status.name if record.delivery_status else '',
                'shipment_term_id': record.shipment_term_id.name if record.shipment_term_id else '',
                'done': record.done,
                'notify': record.notify,
                'form_id':record.shipment_term_id.id,
                 'name':record.shipment_term_id.name
            }
            print("ooooooooooooooooooooo",data)

        # Pass the created record values to FetchData

        else:
            print('blooper')

        return record

    def write(self, vals):
        record_ids = self.ids
        old_values_dict = {rec.id: rec.read()[0] for rec in self.browse(record_ids)}

        result = super(ShipmentTerms, self).write(vals)
        new_values_dict = {rec.id: rec.read()[0] for rec in self.browse(record_ids)}

        updated_fields_list = []  # Initialize a list to store updated fields

        for record_id in record_ids:
            old_values = old_values_dict[record_id]
            new_values = new_values_dict[record_id]

            # Find the fields that have been updated
            updated_values = {field: {'old_value': old_values[field], 'new_value': new_values[field]}
                              for field in vals if new_values[field] != old_values[field]}

            if updated_values:
                # Convert the old and new values to field names
                formatted_updated_values = {
                    field: {
                        'old_value': f'{field} ({old_values[field]})',
                        'new_value': f'{field} ({new_values[field]})'
                    }
                    for field, values in updated_values.items()
                }

                # Append the updated fields to the list
                updated_fields_list.extend(formatted_updated_values.keys())

                # Call the create_fetch_data method to save the updated values
                fetch_data = self.env['fetch.data'].create_fetch_data({
                    'updated_values': formatted_updated_values,
                    'updated_list': updated_fields_list  # Pass the updated fields list
                })
                print(fetch_data, "fetch_data created and stored")

            # Handle notification logic
            if new_values.get('done') and not old_values.get('notify', False):
                self.browse(record_id).write({'notify': True})
                self.env['fetch.data'].write({"updated_list": updated_fields_list})

        # Optionally, do something with the updated_fields_list here
        print("Updated fields list:", updated_fields_list)

        return result

    @api.onchange('product_id')
    def onchange_prod_id(self):
        if self.product_id:
            self.product_code = self.product_id.default_code

    @api.constrains('product_id')
    def _constrains_pro_id(self):
        if not self.product_id or len(self.product_id) == 0:
            raise ValidationError("You must add at least one product!")

class FetchData(models.Model):
    _name = "fetch.data"

    name = fields.Char(string="Name")
    updated_list = fields.Text(string="Updated list")
    updated_values = fields.Text(string="Updated Values")

    @api.model
    def create_fetch_data(self, data):
        updated_values = data.get('updated_values', {})
        updated_list = data.get('updated_list', [])

        # Format updated values and list as strings for storing in the Text fields
        formatted_values_str = str(updated_values)
        formatted_list_str = ', '.join(updated_list)

        # Log the formatted updated values and list (for debugging purposes)
        print(formatted_values_str)
        print(formatted_list_str)

        # Create and store the FetchData record
        record = super(FetchData, self).create({
            'name': "Updated Values",
            'updated_values': formatted_values_str,
            'updated_list': formatted_list_str,
        })
        print(record.updated_values, "record saved")
        print(record.updated_list, "updated_list saved")

        # Return detailed information about the created record
        return {
            'id': record.id,
            'name': record.name,
            'updated_values': record.updated_values,
            'updated_list': record.updated_list
        }










