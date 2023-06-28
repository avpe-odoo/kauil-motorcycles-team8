from odoo import api, fields, models


class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _inherit = ["motorcycle.registry", "portal.mixin"]

    owner_name = fields.Char(related="owner_id.name", string="Owner Name")
    owner_state = fields.Char(related="owner_id.state_id.name", string="State")
    owner_country = fields.Char(related="owner_id.country_id.name", string="Country")

    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = f"/my/motorcycles/{record.id}"
