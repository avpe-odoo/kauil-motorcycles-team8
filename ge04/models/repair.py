from odoo import api, fields, models


class Repair(models.Model):
    _inherit = "repair.order"

    vin = fields.Char(string="VIN", required=True)
    current_mileage = fields.Integer(string="Current Mileage", required=True)

    registry_number = fields.Many2one(
        comodel_name="motorcycle.registry",
        string="Registry Number",
        compute="_compute_registry_number",
        store=True,
    )

    partner_id = fields.Many2one(related="registry_number.owner_id")
    sale_order_id = fields.Many2one(related="registry_number.sale_order")
    lot_id = fields.Many2one(related="registry_number.lot_id")
    product_id = fields.Many2one(related="lot_id.product_id")

    @api.depends("vin")
    def _compute_registry_number(self):
        for record in self:
            record.registry_number = (
                self.env["motorcycle.registry"]
                .search([("vin", "=", record.vin)], limit=1)
                .lot_id.registry_id
            )

    def action_validate(self):
        self.env["motorcycle.registry"].search([("vin", "=", self.vin)]).write(
            {"current_mileage": self.current_mileage}
        )
        return super(Repair, self).action_validate()
