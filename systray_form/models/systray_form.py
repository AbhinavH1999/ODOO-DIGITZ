from odoo import api, fields,models
from odoo import tools
class SystrayForm(models.Model):
    _name = "systray.forms"
    _description ="systray Records"

    name= fields.Char(string="issue",required=True)
    images= fields.Binary(string='images')
    check= fields.Boolean(string='bool')
    group_id = fields.Many2one('res.groups', string='Group')
    create_uid = fields.Many2one('res.users', index=True)





    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked', 'Checked'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    ], default="draft", string="Status", store=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")


        # return{
        #             'type':'ir.actions.act_window',
        #             'res_model':'systray.forms',
        #             'view_mode': 'tree',
        #             'target':'current',
        #
        #         }
    # user_name = fields.Char(string="User", compute='_compute_user_name', store=True)

    # @api.depends('create_uid')
    # def _compute_user_name(self):
    #     for record in self:
    #         record.user_name = record.create_uid.name

    def draft(self):
        for rec in self:
            rec.state = 'draft'

    def checked(self):
        for rec in self:
            rec.state = 'checked'

    def validated(self):
        for rec in self:
            rec.state = 'validated'

    def rejected(self):
        for rec in self:
            rec.state = 'rejected'


    def my_python_function(self,*args, **kwargs):
        # Implement the logic to determine the value of `check`
        record = self.search([], limit=1, order='id desc')  # Example to get the latest record
        self.check = True  # Activate the 'check' field
        print(record.check)  # Print the check field value for debugging
        # return {'check': record.check}
        return {
            'check': record.check
        }


    def set_check_false(self,*args, **kwargs):
        records = self.search([])  # Modify this search to your specific needs
        records.write({'check': False})
        return True









