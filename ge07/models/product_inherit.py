from odoo import api, fields, models

class ProductInherit(models.Model):
    _inherit = "product.template"

    name = fields.Char('Name', index='trigram', required=True, translate=True,readonly=False,compute="_compute_from_model_make_year",store=True)

    @api.depends('model','make','year')
    def _compute_from_model_make_year(self):
        for record in self:
            print()
            print(record.name)
            print()
            if record.detailed_type=='motorcycle':
                record.name= str(record.year)+" "+str(record.make)+" "+str(record.model)
            else:
                record.name=record.name
    # @api.onchange("detailed_type")
    # def onChangeDetailedType(self):
    #     for record in self:
    #         if record.detailed_type == "motorcycle":
    #             record.name= str(record.year)+" "+str(record.make)+" "+str(record.model)   

    # @api.onchange("model")
    # def onChangeDetailedType(self):
    #     for record in self:
    #         if record.detailed_type == "motorcycle":
    #             record.name= str(record.year)+" "+str(record.make)+" "+str(record.model)   

    # @api.onchange("make")
    # def onChangeDetailedType(self):
    #     for record in self:
    #         if record.detailed_type == "motorcycle":
    #             record.name= str(record.year)+" "+str(record.make)+" "+str(record.model)   