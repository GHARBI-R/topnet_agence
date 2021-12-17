from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class Rdv(models.Model):
    _name = 'rdv'
    _description = 'rendez-vous'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rdv_id = fields.Char(string='Rendez-vous reference', required=True, copy=False, readonly=True,
                         default=lambda self: _('New'))

    rdv_clt = fields.Many2one(comodel_name='client.fiche', string='Rendez_vous')
    rdv_raison_rel = fields.Char(string='Raison sociale', related='rdv_clt.raison')
    email_clt_rel = fields.Char(string='Email principal ', related='rdv_clt.email_pri')

    abonnement_rdv = fields.Many2one(comodel_name='abonnement', string='Abonnement')
    abonnement_rel = fields.Char(string='Abonnement N° ', related='abonnement_rdv.id_abonnement')

    motif = fields.Text(string='motif du rendez-vous', required=True)
    rdv_date_debut = fields.Datetime(string='Date Debut')
    rdv_date_fin = fields.Datetime(string='Date fin')
    client_id = fields.Many2one(comodel_name='client.fiche', string='Client', readonly=True)
    agent_id = fields.Many2one(comodel_name='agent.fiche', string='Agent')

    # @api.constrains('rdv_date_debut', 'rdv_date_fin')
    # def _check_date(self):
    #     if self.rdv_date_debut > self.rdv_date_fin:
    #         raise ValidationError('End date must be greater than start date')

    @api.constrains('rdv_date_debut','rdv_date_fin')
    def _check_rdv_date_debut(self):
        if self.rdv_date_debut < datetime.today():
            raise ValidationError('la date début doit être supérieur à la date actuelle')
        if self.rdv_date_fin < datetime.today():
            raise ValidationError('la date fin doit être supérieur à la date actuelle')
        if self.rdv_date_fin < self.rdv_date_debut:
            raise ValidationError('la date fin doit être supérieur à la date debut')

    @api.model
    def create(self, vals):
        if vals.get('rdv_id', _('New')) == _('New'):
            vals['rdv_id'] = self.env['ir.sequence'].next_by_code('topnet.rdv.seq') or _('New')
        result = super(Rdv, self).create(vals)
        return result
