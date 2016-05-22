import json

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from django.views.generic import TemplateView

from .models import Selector, Outages


class DashboardView(TemplateView):

    template_name = "events/dashboard.html"

    def __init__(self):
        TemplateView.__init__(self)
        self.probes = None
        self.outages = []
        self.now = datetime.utcnow() - relativedelta(days=1)

    def get_context_data(self, **kwargs):
        """
        Generating variables that end up in the view goes here.
        """

        context = TemplateView.get_context_data(self, **kwargs)

        self.now = kwargs.get("date", self.now) or self.now
        if "date" in kwargs and kwargs["date"]:
            self.now = parse(kwargs["date"])

        self.probes = Selector.factory(kwargs["selector"]).get_probes()
        self.outages = Outages(
            self.now,
            self.now + relativedelta(days=1),
            self.probes,
            900,
            0.01
        )

        context["date"] = kwargs.get("date", "")
        context["selector"] = kwargs["selector"]
        context["geography"] = self.get_geojson()
        context["outages"] = self.outages.get()
        context["log"] = self.get_connection_log(self.outages.events)
        context["name"] = Selector.get_name(kwargs["selector"])

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

    def get_connection_log(self, events):

        r = {
            "x": ["x"],
            "connect": ["connect"],
            "disconnect": ["disconnect"]
        }

        for t in range(events[0]["timestamp"] + 900, events[-1]["timestamp"], 900):
            r["x"].append(datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S"))
            counters = {
                "connect": 0,
                "disconnect": 0
            }
            for event in events:
                if t - 900 <= event["timestamp"] <= t:
                    counters[event["event"]] += 1
            r["connect"].append(counters["connect"])
            r["disconnect"].append(counters["disconnect"])

        return json.dumps(r, separators=(",", ":"))
