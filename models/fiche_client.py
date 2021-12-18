# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class Clients(models.Model):
    _name = 'client.fiche'
    _description = 'fiche clients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    _sql_constraints = [
        ('cin_pass_uniq', 'unique(cin_pass)', 'Numero de cin/passeport existe déja'),
        ('email_admi_uniq', 'unique(email_admi)', 'Email existe déja'),
        ('email_tech_uniq', 'unique(email_tech)', 'Email existe déja'),
        ('email_pri_uniq', 'unique(email_pri)', 'Email existe déja'),
    ]


    # @api.model
    # def create(self, vals):
    #     if vals.get('id_abonnement', _('New')) == _('New'):
    #         vals['id_abonnement'] = self.env['ir.sequence'].next_by_code('topnet.abonnement.sequence') or _('New')
    #     result = super(Abonnements, self).create(vals)
    #     return result

    @api.model
    def contrat(self, vals):
        if vals.get('id_contrat', _('New')) == _('New'):
            vals['id_contrat'] = self.env['ir.sequence'].next_by_code('topnet.client.code') or _('New')
        result = super(Clients, self).create(vals)
        return result

    id_contrat = fields.Char(string='Code client ', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))


    user_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    abonnements_ids = fields.One2many(comodel_name='abonnement', inverse_name='raison_clt', string="Abonnements")
    contrat_ids = fields.One2many(comodel_name='abonnement', inverse_name='contrat_clt', string="contrat")

    dossiers_ids = fields.One2many(comodel_name='topnet.dossier', inverse_name='raison_clt1', string="Dossier")

    rdvs_ids = fields.One2many(comodel_name='rdv', inverse_name='rdv_clt', string="Rendez-vous")


    role = fields.Char(string="role", default="Client")
    name = fields.Char(string="Nom et Prénom du gérant", track_visibility="always")
    cin_pass = fields.Integer(string="Numéro CIN/Passeport")
    email_pri = fields.Char(string="Email principale")
    raison = fields.Char(string="Raison sociale")
    registre = fields.Char(string="Registre de commerce")
    tva = fields.Integer(string="Code TVA")
    Exonéré = fields.Selection([("oui", "Oui"), ("non", "Non")])
    douane = fields.Integer(string="Code en douane")
    activity = fields.Selection([("commerciale", "Commerciale"), ("Administratif", "Administratif"),
                                 ("agricole", "Agricole"), ("touristique", "Touristique")], required=True)
    correspondance = fields.Char(string="Adresse de correspondance")
    Ville = fields.Char(string="Ville")
    postale = fields.Integer(string="Code postale")
    tel = fields.Integer(string="Tél")
    fax = fields.Integer(string="Fax")

    #  Contact Administratif et Financiers

    nom = fields.Char(string="Nom et Prénom")
    Tel_admi = fields.Integer(string="Tél")
    gsm_admi = fields.Integer(string="GSM")
    email_admi = fields.Char(string="Email")

    #  Contact technique

    nom_tech = fields.Char(string="Nom et Prénom")
    tel_tech = fields.Integer(string="Tél")
    gsm_tech = fields.Integer(string="GSM")
    email_tech = fields.Char(string="Email")

    active = fields.Boolean(string="Active", default=True)

    @api.constrains('name', 'tel', 'fax', 'Tel_admi', 'gsm_admi', 'nom_tech', 'tel_tech',
                    'gsm_tech')
    def check_name(self):
        for rec in self:
            if len(str(abs(self.tel))) != 8:
                raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))

            elif len(str(abs(self.fax))) != 8:
                raise ValidationError(_('Nméro de fax doit contenir seulement 8 chiffres'))
            elif len(str(abs(self.Tel_admi))) != 8:
                raise ValidationError(_('Nméro de tel administratif doit contenir seulement 8 chiffres'))
            elif len(str(abs(self.gsm_admi))) != 8:
                raise ValidationError(_('Nméro de gsm administratif  doit contenir seulement 8 chiffres'))
            elif len(str(abs(self.tel_tech))) != 8:
                raise ValidationError(_('Nméro de tel technique doit contenir seulement 8 chiffres'))
            elif len(str(abs(self.gsm_tech))) != 8:
                raise ValidationError(_('Nméro de gsm technique doit contenir seulement 8 chiffres'))
            elif len(self.name) > 30:
                raise ValidationError(_('Nom du gérant trop long'))
            elif len(self.nom_tech) > 30:
                raise ValidationError(_('Nom Technique trop long'))

    @api.constrains('email_admi', 'email_tech', 'email_pri')
    def validate_email(self):
        for obj in self:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email_pri) == None:
                raise ValidationError("Vérifier votre adresse mail principale : %s" % obj.email_pri)
            elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email_admi) == None:
                raise ValidationError("Vérifier votre adresse mail administratif: %s" % obj.email_admi)
            elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email_tech) == None:
                raise ValidationError("Vérifier votre adresse mail technique : %s" % obj.email_tech)

        return True


    @api.model
    def create(self, values):
        vals_user = {
            'name': values.get('name'),
            'login': values.get('email_pri'),

            # other required field
        }
        user_id = self.env['res.users'].sudo().create(vals_user)
        values.update(user_id=user_id.id)
        res = super(Clients, self).create(values)

        return res

    @api.depends()
    def action_ab(self):
        return {
            'name': _('Demande Abonnement'),
            'domain': [('user_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'abonnement',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }

