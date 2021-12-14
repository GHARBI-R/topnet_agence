
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class Agent(models.Model):
    _name = 'agent.fiche'
    _description = 'fiche agent'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nom'

    _sql_constraints = [
        ('cin_pass_uniq', 'unique(num_cin_num_passeport)', 'Numero de cin/passeport existe déja'),
        ('email_uniq', 'unique(email)', 'Email existe déja'),
        ('matricule_uniq', 'unique(matricule)', 'matricule existe déja'),]

    def action_disponible(self):
        for rec in self:
            rec.state = 'disponible'

    def action_abscent(self):
        for rec in self:
            rec.state = 'abscent'

    user_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    abonnements_ids = fields.One2many(comodel_name='abonnement', inverse_name='agent_id', string="agent")
    rdv_ids = fields.One2many(comodel_name='rdv', inverse_name='rdv_clt', string="Rendez-vous")

    nom = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prenom", required=True)
    adresse = fields.Char(string="Adresse", required=True)
    naissance = fields.Date(string="Date de naissance", required=True)
    num_cin_num_passeport = fields.Integer(string=" N°cin / N°passeport", required=True)
    matricule = fields.Char(string="Matricule", required=True)
    email = fields.Char(string="Email", required=True, track_visibility="always")
    mot_passe = fields.Char(string="Mot de passe", required=True)
    c_mot_passe = fields.Char(string="Confirmation Mot de passe", required=True)
    telephone = fields.Integer(string="Téléphone")
    role = fields.Selection([("administrateur", "Administrateur"), ("responsable agences", "Responsable agences"),
                             ("chef agence", "Chef agence"), ("agent", "Agent")], required=True, track_visibility="always")

    Nom_agence = fields.Many2one('topnet.agence', string='Agence')
    agence_deleg = fields.Selection('Delegation', related='Nom_agence.Delegation')
    agence_Adresse = fields.Char('Adresse', related='Nom_agence.Adresse')
    agence_Fax = fields.Integer('Fax', related='Nom_agence.Fax')
    active = fields.Boolean("Active", default=True)
    image = fields.Binary(string="Image", attachment=True)
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('abscent', 'Abscent'),
    ], string='Status', readonly=True, default='disponible')

    @api.constrains('name', 'telephone', 'mot_passe', 'c_mot_passe')
    def check_name(self):
        for rec in self:
            if len(str(abs(self.telephone))) != 8:
                raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))
            elif (self.mot_passe) != (self.c_mot_passe):
                raise ValidationError(_('mot de passe et confirmation mot de passe doivent être identique '))
            elif len(self.nom) > 20:
                raise ValidationError(_('Nom  trop long'))

    @api.constrains('email')
    def validate_email(self):
        for obj in self:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email) == None:
                raise ValidationError("Vérifier votre adresse mail principale : %s" % obj.email)


        return True

    @api.model
    def create(self, values):
        vals_user = {
            'name': values.get('nom'),
            'login': values.get('email'),
            'password': values.get('mot_passe'),
            'id': values.get('agent_id')

        }
        user_id = self.env['res.users'].sudo().create(vals_user)
        values.update(user_id=user_id.id)
        res = super(Agent, self).create(values)

        return res