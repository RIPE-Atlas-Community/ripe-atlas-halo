import json

from datetime import datetime
from dateutil.parser import parse

from django.views.generic import TemplateView

from .models import Selector


class DashboardView(TemplateView):

    template_name = "events/dashboard.html"

    def __init__(self):
        TemplateView.__init__(self)
        self.probes = None
        self.t = datetime.utcnow()

    def get_context_data(self, **kwargs):
        """
        Generating variables that end up in the view goes here.
        """

        if "t" in self.request.GET:
            self.t = parse(self.request.GET["t"])

        context = TemplateView.get_context_data(self, **kwargs)

        self.probes = Selector.factory(kwargs["selector"]).get_probes()

        context["geography"] = self.get_geojson()

        # Modify context here

        return context

    def get_geojson(self):

        r = []
        for probe in self.probes:
            r.append({
                "type": "Feature",
                "geometry": probe.geometry,
                "properties": {
                    "id": probe.id,
                    "marker-size": "large",
                    "marker-color": "#199638",
                    "marker-style": "star"
                }
            })

        print(json.dumps(r, indent=2, separators=(",", ":")))
        return json.dumps(r, separators=(",", ":"))
