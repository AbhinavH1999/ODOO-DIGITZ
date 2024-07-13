from odoo import api, fields,models

class DeliveryOrder(models.Model):
    _name = "delivery.order"
    _description ="order delivery"

    name= fields.Char(string="Name",required=True)



    def action_test13(self):
        pass

