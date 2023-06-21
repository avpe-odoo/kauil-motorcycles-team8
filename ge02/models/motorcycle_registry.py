from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    lot_id = fields.One2many(
        comodel_name="stock.lot",
        inverse_name="registry_id",
        string="Lot ID",
        required=False,
        ondelete="cascade",
    )

    @api.constrains("stock_lot")
    def _check_stock_lot(self):
        for record in self:
            if len(record.lot_id) > 1:
                raise ValidationError("Stock lot must be unique.")
