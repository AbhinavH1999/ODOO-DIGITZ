from odoo import fields, models, api


class Incoterms(models.Model):
    _name = 'inco.terms'

    name = fields.Char('Name')
