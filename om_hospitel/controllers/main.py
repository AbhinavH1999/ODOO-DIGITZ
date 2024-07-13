from odoo import http
from odoo.http import request
class Hospital(http.Controller):
    @http.route('/hospital/doctor/',website=True,auth='public')
    def hospital_doctor(self):
        # return "hello,world"
        patients=request.env['sale.order'].sudo().search([])
        print('patient ----',patients)
        return request.render("om_hospitel.patients_page", { 'patients':patients})