from odoo import api, fields,models

class HospitalDoctors(models.Model):
    _name = "hospital.doctors"
    _description ="doctors Records"

    name= fields.Char(string="Name",required=True)
    age= fields.Integer(string="Age")
    appointment_ids=fields.One2many('hospital.patient','pharmacy_id',string='children')

    # this for
    @api.onchange('appointment_ids')
    def action_test(self):
        ID = 73
        for rec in self:

            list=[
                (4,ID)
            ]

            rec.appointment_ids=list




    # def action_test(self):
    #     id=64
    #     link=self.env['hospital.patient'].search([
    #         'id','=',self.
    #     ])




