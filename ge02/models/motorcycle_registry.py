from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    lot_ids = fields.One2many(
        comodel_name="stock.lot",
        inverse_name="registry_id",
        string="Lot IDs",
        ondelete="cascade",
        store=True,
    )

    lot_id = fields.Many2one(
        compute="_compute_lot_id",
        comodel_name="stock.lot",
        string="Lot ID",
        store=True,
    )

    vin = fields.Char(related="lot_id.name")

    @api.depends("lot_ids")
    def _compute_lot_id(self):
        for record in self:
            if not record.lot_ids:
                raise ValidationError("No stock lot found.")
            record.lot_id = record.lot_ids[0]

    @api.constrains("lot_ids")
    def _check_lot_ids(self):
        for record in self:
            motorcycles = self.env["motorcycle.registry"].search(
                [("vin", "=", record.vin)]
            )
            if len(motorcycles) > 1:
                raise ValidationError("Only one stock lot is allowed.")
