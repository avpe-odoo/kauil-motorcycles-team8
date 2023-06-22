from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if self.env["sale.order"].search([("name", "=", self.origin)]).state == "sale":
            move_line_id = (
                self.env["stock.move.line"]
                .search([("picking_id", "=", self.id)])
                .lot_id.name
            )
            self.env["motorcycle.registry"].create(
                {
                    "vin": move_line_id,
                    "owner_id": self.partner_id.id,
                }
            )
        return super(Picking, self).button_validate()
