from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def _get_next_serial(self, company, product):
        product_type = product.product_tmpl_id.detailed_type
        if product.tracking != "none" and product_type == "motorcycle":
            prefix = product.make + product.model + str(product.year)[-2:]+str(product.battery_capacity).upper()
            return prefix + self.env["ir.sequence"].next_by_code("stock.lot.serial")
        else:
            return super(StockLot, self)._get_next_serial(company, product)
