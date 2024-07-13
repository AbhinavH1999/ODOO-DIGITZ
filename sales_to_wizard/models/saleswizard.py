from odoo import fields,models

class SalesWizard(models.Model):
    _inherit='sale.order'

    bio=fields.Char(String="bio")

    def action_test16(self):
        list=[]
        for rec in self.order_line:
            list.append(
                {
                    'product':rec.product_id.id,
                    'description':rec.name,
                    'quantity':rec.product_uom_qty,
                    'line_id':rec.id
                }
            )

        return {
            'view_mode': 'form',
            'res_model': 'wizards.sales',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_order_line_ids': list}
             }