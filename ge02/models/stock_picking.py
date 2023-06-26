from odoo import api, fields, models, Command


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(Picking, self).button_validate()
        for picking in self:
            state = self.env["sale.order"].search([("name", "=", picking.origin)]).state
            if state == "sale":
                for move in picking.move_line_ids:
                    if move.product_id.product_tmpl_id.detailed_type == "motorcycle":
                        self.env["motorcycle.registry"].create(
                            {
                                "lot_ids": [Command.link(move.lot_id.id)],
                                "sale_order": picking.sale_id.id,
                            }
                        )
        return res
