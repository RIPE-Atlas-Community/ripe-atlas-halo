import json

from django.views.generic import TemplateView

from .models import Selector, Event


class DashboardView(TemplateView):

    template_name = "events/dashboard.html"

    def __init__(self):
        TemplateView.__init__(self)
        self.probes = None
        self.connection_log = []

    def get_context_data(self, **kwargs):
        """
        Generating variables that end up in the view goes here.
        """

        context = TemplateView.get_context_data(self, **kwargs)

        self.probes = Selector.factory(kwargs["selector"]).get_probes()

        context["geography"] = self.get_geojson()
        context["log"] = self.get_connection_log()
        print(context["log"])

        return context

    def get_geojson(self):

        r = []
        for probe in self.probes:
            r.append({
                "type": "Feature",
                "geometry": probe.geometry,
                "properties": probe.meta_data
            })

        return json.dumps(r, separators=(",", ":"))

    def get_connection_log(self):
        return json.dumps(
            Event.get_raw_data(
                sorted(list(self.probes), key=lambda x: x["timestamp"])[:300]
            ),
            separators=(",", ":"),
            indent=2
        )
