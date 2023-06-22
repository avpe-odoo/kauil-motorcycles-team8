from odoo import api, fields, models

class ProductInherit(models.Model):
    _inherit = "product.template"

    name = fields.Char('Name', index='trigram', required=True, translate=True,compute='_compute_from_model_make_year')

    @api.depends('model','make','year')
    def _compute_from_model_make_year(self):
        for record in self:
            if record.detailed_type=='motorcycle':
                record.name= str(record.year)+" "+str(record.make)+" "+str(record.model)
            else:
                record.name=""