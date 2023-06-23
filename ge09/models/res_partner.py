from odoo import api, models, fields

class Partner(models.Model):
    _inherit = ['res.partner']

    is_new_customer = fields.Boolean()