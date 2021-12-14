from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class Rdv (models.Model):
    _name = 'rdv'
    _description = 'rendez-vous'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rdv_id = fields.Char(string='Rendez-vous reference', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))

    rdv_clt = fields.Many2one(comodel_name='client.fiche', string='Rendez_vous')
    rdv_raison_rel = fields.Char(string='Raison sociale', related='rdv_clt.raison')
    email_clt_rel = fields.Char(string='Email principal ', related='rdv_clt.email_pri')

    motif = fields.Text( string='motif du rendez-vous', required=True)
    rdv_date_debut = fields.Datetime(string='Date Debut')
    rdv_date_fin = fields.Datetime(string='Date fin')
    client_id = fields.Many2one(comodel_name='client.fiche', string='Client', readonly=True)
    agent_id = fields.Many2one(comodel_name='agent.fiche', string='Agent')



    @api.model
    def create(self, vals):
        if vals.get('rdv_id', _('New')) == _('New'):
            vals['rdv_id'] = self.env['ir.sequence'].next_by_code('topnet.rdv.seq') or _('New')
        result = super(Rdv, self).create(vals)
        return result


