# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class Abonnements (models.Model):
    _name = 'abonnement'
    _description = 'demande abonnement  '
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'name'


    @api.model
    def create(self, vals):
        if vals.get('id_abonnement', _('New')) == _('New'):
            vals['id_abonnement'] = self.env['ir.sequence'].next_by_code('topnet.abonnement.sequence') or _('New')
        result = super(Abonnements, self).create(vals)
        return result

    def action_pris(self):
        for rec in self:
            rec.state = 'pris'

    def action_valider(self):
        for rec in self:
            rec.state = 'valider'

    def action_non_valider(self):
        for rec in self:
            rec.state = 'non_valider'

    @api.depends('state')
    def action_depot(self):
         for rec in self:
            if rec.state == 'raccord':
               return {
                  'name': _('Déposer'),
                  'domain': [('user_id', '=', self.id)],
                  'view_type': 'form',
                  'res_model': 'topnet.dossier',
                  'view_id': False,
                  'view_mode': 'form',
                  'type': 'ir.actions.act_window',
                  }
               for rec in self:
                  rec.state = 'dossier'

    def action_raccord(self):
        for rec in self:
           if rec.state == 'valider':
              rec.state ='raccord'

    state = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('pris', 'Prise en charge'),
        ('valider', 'Valide'),
        ('raccord', 'Frais de raccordement'),
        ('non_valider', 'Non valide'),
        ('dossier', 'Dépot Dossier'),

    ], string='Status', readonly=True, default='nouveau')

    id_abonnement = fields.Char(string='Numéro abonnement', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))

    etat = fields.Selection(
        [("contrat en cours de traitement coté topnet", "Contrat en cours de traitement coté topnet"),
         ("Etude", "Etude"),
         ("contrat rejeté par topnet", "Contrat rejeté par topnet"),
         ("contrat rejeté par TT", "Contrat rejeté par TT"),
         ("contrat validé par topnet", "Contrat validé par topnet"),
         ("ligne installé par TT", "ligne installé par TT"),
         ("demande TV", "Demande d'abonnement traitée et clotûrée"),
         ("initiale", "Etat Initiale")] , default="initiale", string="Etat du dossier")

    client_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    raison_clt= fields.Many2one(comodel_name='client.fiche', string='raison')
    raison_clt_rel= fields.Char (string='Raison sociale', related='raison_clt.raison')

    agent_id = fields.Many2one(comodel_name='agent.fiche', string='Agent')
    agent_rel = fields.Char(string='Agent ', related='agent_id.nom')

    contrat_clt = fields.Many2one(comodel_name='client.fiche', string='contrat')
    contrat_clt_rel = fields.Char(string='numéro de contrat', related='contrat_clt.id_contrat')
    installation = fields.Char(string="Adresse d'installation", required=True)
    ville2 = fields.Char(string="Ville" ,required=True)
    postale2 = fields.Integer(string="Code postale", required=True)
    tel2 = fields.Integer(string="Tél")
    fax2 = fields.Integer(string="Fax")

    type_offre = fields.Selection(
        [('Fibre Optique', 'Fibre Optique'), ('Voip Access', 'Voip Access'), ('Rapido Pro', 'Rapido Pro')],
        default="Fibre Optique", required=True)
    debit = fields.Selection([("20", "20"), ("30", "30"), ("50", "50"), ("100", "100")], default="20", required=True)
    abonnement_date = fields.Date(string='Date',default=datetime.today(),  readonly=True)
    @api.constrains('tel2', 'fax2')
    def check_name(self):
        for rec in self:

            if len(str(self.tel2)) != 8:
                raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))
            elif len(str(self.fax2)) != 8:
                raise ValidationError(_('Nméro de fax doit contenir seulement 8 chiffres'))
