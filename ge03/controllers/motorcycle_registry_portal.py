from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class MotorcycleRegistryPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = self._prepare_motorcycle_registry_domain(request.env.user.partner_id)

        MotorcycleRegistry = request.env["motorcycle.registry"]
        if "motorcycle_count" in counters:
            values["motorcycle_count"] = (
                MotorcycleRegistry.search_count(domain)
                if MotorcycleRegistry.check_access_rights("read", raise_exception=False)
                else 0
            )

        return values

    def _prepare_motorcycle_registry_domain(self, partner):
        return [
            "|",
            ("owner_id", "=", partner.id),
            ("is_public", "=", True),
        ]

    def _get_motorcycle_registry_searchbar_sortings(self):
        return {
            "name": {"label": _("Owner Name"), "order": "owner_name"},
            "state": {"label": _("State"), "order": "owner_state"},
            "country": {"label": _("Country"), "order": "owner_country"},
            "make": {"label": _("Make"), "order": "make"},
            "model": {"label": _("Model"), "order": "model"},
        }

    def _prepare_motorcycle_registry_portal_rendering_values(
        self,
        page=1,
        sortby=None,
        **kwargs,
    ):
        MotorcycleRegistry = request.env["motorcycle.registry"]

        if not sortby:
            sortby = "name"

        values = self._prepare_portal_layout_values()

        url = "/my/motorcycles"
        domain = self._prepare_motorcycle_registry_domain(request.env.user.partner_id)

        searchbar_sortings = self._get_motorcycle_registry_searchbar_sortings()
        sort_order = searchbar_sortings[sortby]["order"]

        pager_values = portal_pager(
            url=url,
            total=MotorcycleRegistry.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"sortby": sortby},
        )

        motorcycles = MotorcycleRegistry.search(
            domain,
            order=sort_order,
            limit=self._items_per_page,
            offset=pager_values["offset"],
        )

        values.update(
            {
                "motorcycles": motorcycles.sudo(),
                "page_name": "motorcycles",
                "pager": pager_values,
                "default_url": url,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )

        return values

    @http.route(
        ["/my/motorcycles", "/my/motorcycles/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_motorcycles(self, **kwargs):
        values = self._prepare_motorcycle_registry_portal_rendering_values(**kwargs)
        request.session["my_motorcycles_history"] = values["motorcycles"].ids[:100]
        return request.render("ge03.portal_my_motorcycles", values)

    @http.route(
        ["/my/motorcycles/<int:motorcycle_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_motorcycle_registry_page(
        self,
        motorcycle_id,
        access_token=None,
        message=False,
        **kwargs,
    ):
        try:
            motorcycle_sudo = self._document_check_access(
                "motorcycle.registry", motorcycle_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        backend_url = (
            f"/web#model={motorcycle_sudo._name}"
            f"&id={motorcycle_sudo.id}"
            f"&view_type=form"
        )

        values = {
            "motorcycle": motorcycle_sudo,
            "message": message,
            "report_type": "html",
            "backend_url": backend_url,
        }

        values = self._get_page_view_values(
            motorcycle_sudo, access_token, values, "my_motorcycles_history", False
        )

        return request.render("ge03.motorcycle_registry_portal_template", values)

    @http.route(
        "/my/motorcycles/submit",
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
        csrf=False,
    )
    def test_path(self, **kwargs):
        motorcycle_id = kwargs.get("id")
        is_public = kwargs.get("is_public") != None

        request.env["motorcycle.registry"].search([("id", "=", motorcycle_id)]).write(
            {"is_public": is_public}
        )
