from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if self.env["sale.order"].search([("name", "=", self.origin)]).state == "sale":
            lot_record = (
                self.env["stock.move.line"]
                .search([("picking_id", "=", self.id)])
                .lot_id.name
            )
            self.env["motorcycle.registry"].create(
                {
                    "vin": lot_record.name,
                    "owner_id": self.partner_id.id,
                    "lot_id": lot_record,
                }
            )
        return super(Picking, self).button_validate()
