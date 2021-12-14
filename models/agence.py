# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Agence (models.Model):
    _name = 'topnet.agence'
    _description = 'les agences topnet'
    _rec_name = 'Nom_agence'

    Nom_agence = fields.Selection([("Topnet Agence centre urbain nord", "Topnet Agence centre urbain nord"),
                               ("Topnet Agence Tunis", "Topnet Agence Tunis"),
                               ("Topnet Agence Bardo", "Topnet Agence Bardo"),
                               ("Topnet Agence Ennasr", "Topnet Agence Ennasr"),
                               ("Topnet Agence La Marsa", "Topnet Agence La Marsa"),
                               ("Topnet Agence Le Passage", "Topnet Agence Le Passage"),
                               ("Topnet Agence Bizerte", "Topnet Agence Bizerte"),
                               ("Topnet Agence Nabeul", "Topnet Agence Nabeul"),
                               ("Topnet Agence Khzema", "Topnet Agence Khzema"),
                               ("Topnet Agence Sousse", "Topnet Agence Sousse"),
                               ("Topnet Agence Monastir", "Topnet Agence Monastir"),
                               ("Topnet Agence Sfax", "Topnet Agence Sfax"),
                               ("Topnet Agence Taib Mhiri Sfax", "Topnet Agence Taib Mhiri Sfax"),
                               ("Topnet Agence El Mourouj", "Topnet Agence El Mourouj"),
                               ("Topnet Agence Gabes", "Topnet Agence Gabes")], required=True)

    Delegation= fields.Selection([("ariana", "Ariana"), ("beja", "Béja"), ("ben_Arous", "Ben Arous"), ("bizerte", "Bizerte"), ("gabes", "Gabés"), ("gafsa", "Gafsa"), ("jendouba", "Jendouba"), ("kairouan", "Kairouan"), ("kasserine", "Kasserine"), ("kébili", "Kébili"), ("le_Kef", "Le Kef"), ("mahdia", "Mahdia"), ("la_Manouba", "La Manouba"), ("mednine", "Médenine"), ("monastir", "Monastir"), ("nabeul", "Nabeul"), ("sfax", "Sfax"), ("sidi_Bouzid", "Sidi Bouzid"), ("siliana", "Siliana"), ("sousse", "Sousse"), ("tataouine", "Tataouine"), ("tozeur", "Tozeur"), ("tunis", "Tunis"), ("zaghouan", "Zaghouan")], required=True, string="Delegation")
    Adresse = fields.Char(string="Adresse", required=True)
    Fax = fields.Integer(string="Fax", required=True)



    @api.constrains('Adresse', 'Fax')
    def check_name(self):
        for rec in self:
            if len(str(abs(self.Fax))) != 8:
                raise ValidationError(_('Numéro de fax doit contenir seulement 8 chiffres'))
            elif len(self.Adresse) > 20:
                raise ValidationError(_('Adresse  trop longue'))
