from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if self.env["sale.order"].search([("name", "=", self.origin)]).state == "sale":
            print()
            print(self.env["stock.lot"]
                    .search([("name", "=", self.name)])
                    .product_id)
            print(self.name)
            print()
            self.env["motorcycle.registry"].create(
                {
                    "vin": self.env["stock.lot"]
                    .search([("name", "=", self.name)])
                    .product_id,
                }
            )
