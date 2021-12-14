
from odoo import http
from odoo.http import request



class Topnet(http.Controller):
    # Sample Controller Created
    @http.route('/topnet/client/', website=True, auth='public')
    def university_student(self, **kw):
        return http.request.render("topnet_agence.client_page", {
        })\



    # creation dans la base de données
    @http.route('/creer/client', type="http", auth='public', website=True)
    def creeruser(self, **kw):
        vals_user = {
            'name': kw.get('name'),
            'login': kw.get('email_pri'),
        }

        res = http.request.env['res.users'].sudo().create(vals_user)
        kw.update({'user_id':res})
        http.request.env['client.fiche'].sudo().create(kw)
        return http.request.render('topnet_agence.client_page_thanks', {})
