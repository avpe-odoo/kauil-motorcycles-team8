from odoo import api, fields, models


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    repair_order_ids = fields.One2many(
        comodel_name="repair.order",
        inverse_name="registry_number",
        string="Repair Orders",
    )

    repair_order_count = fields.Integer(compute="_compute_repair_order_count")

    def action_view_repair_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Repair Orders",
            "view_mode": "tree,form",
            "res_model": "repair.order",
            "domain": [("registry_number", "=", self.id)],
        }

    @api.depends("repair_order_ids")
    def _compute_repair_order_count(self):
        for record in self:
            record.repair_order_count = len(record.repair_order_ids)
