from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"
    
    def button_validate(self):
        print()
        print(self.move_line_ids)
        print(self.env["stock.move.line"])
        if self.env["sale.order"].search([("name", "=", self.origin)]).state == "sale":
            print()
            print(self.move_line_ids)
            temp_moveline_id=self.env["stock.move.line"].search([("picking_id", "=", self.id)]).lot_id.name
            temp_partner_id=self.env["res.partner"]
            print("LOLWA")
            print(temp_moveline_id)
            print("CHUl")
            print(self.partner_id.name)
            self.env["motorcycle.registry"].create(
                {
                    "vin": temp_moveline_id,
                    "owner_id":self.partner_id.id
                }
            )
