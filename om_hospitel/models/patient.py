# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description="Patient Records"

    name = fields.Char(string="Name",required=True,)
    age=fields.Integer(string="Age",tracking=True)
    is_child=fields.Boolean(string="Is Child ?",tracking=True)
    notes=fields.Text(string="Notes")
    gender=fields.Selection([('male','Male'),('female','Female'),('others','Others')],String="Gender",tracking=True)
    capitalized_name = fields.Char(string='capitalized Name ',compute='_compute_capitalized_name',store=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    doctors_id = fields.Many2one('hospital.doctors', string="Doctors")
    product_id = fields.Char(string="product")
    price_unit = fields.Float(string="price")
    qty = fields.Integer(string="quantity")
    pharmacy_id=fields.Many2one('hospital.doctors',string='Appointment',ondelete='cascade')
    tag_ids=fields.Many2many('hospital.doctors','hospital_patient_tag','patient_id','tag_id',string='Tags')
    state=fields.Selection([
        ('new','New'),
        ('processing', 'processing'),
        ('Completed', 'Completed'),
    ],default="new" ,string="Status",store=True)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            seq = self.env['ir.sequence'].next_by_code('hospital.patient')
            print(seq,'ubytgvbty')
            vals['ref'] = seq
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.name:
                rec.capitalized_name=rec.name.upper()
            else:
                rec.capitalized_name=''
    @api.constrains('is_child','age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child  and rec.age == 0:
                raise ValidationError(_("Age hase to be recorded !"))

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child= True
        else:
            self.is_child=False

    # def action_test1(self):
    #     for rec in self:
    #         doctor=rec.doctors_id
    #         print("name:",doctor.name)
    #         print("age:",doctor.age)

    # def action_test1(self):
    #     for rec1 in self.doctors_id:
    #         for rec in rec1.appointment_ids:
    #             product=f'{rec.product_id},{rec.price_unit},{rec.qty}'
    #             print(product)
    #
    def action_test1(self):
        f=self.env['hospital.doctors'].search([],limit=1)
        if f:
            self.doctors_id=f

    # def action_test1(self):
    #     id = 7
    #     self.update( {'doctors_id':id})


        # return {
        #     'name': _('hospital.patient'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hospital.doctors',
        #     'view_mode': 'tree',
        #     'domain': [('id', 'in', self.doctors_id.ids)],
        #     }

    # def action_test1(self):
    #     doctors=self.env['hospital.doctors'].search([])
    #     self.tag_ids=doctors

    # @api.onchange('gender')
    # def _name_(self):
    #     for rec in self:
    #         if rec.gender:
    #             rec.name = rec.gender.capitalize()
    #         else:
    #             rec.name = ''
    def new_(self):
        for rec in self:
            rec.state='new'
    def processing(self):
        for rec in self:
            rec.state = 'processing'

    def Completed(self):
        for rec in self:
            rec.state = 'Completed'




