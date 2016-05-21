from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from django.views.generic import TemplateView

from ripe.atlas.cousteau import AtlasResultsRequest

from django_countries import countries

from ripe.atlas.cousteau import ProbeRequest


class Selector(object):

    def __init__(self, string):
        self.identifier = string

    @classmethod
    def factory(cls, string):
        if string.lower().startswith("as"):
            return AsSelector(string[2:])
        if string.isdigit():
            return AsSelector(string)
        if string.upper() in countries.countries.keys():
            return CountrySelector(string)
        return PrefixSelector(string)


class AsSelector(Selector):

    def __init__(self, string):
        Selector.__init__(self, string)
        self.identifier = int(self.identifier)

    def get_probes(self):
        return ProbeRequest(asn=self.identifier, return_objects=True)


class PrefixSelector(Selector):

    def get_probes(self):
        return ProbeRequest(prefix=self.identifier, return_objects=True)


class CountrySelector(Selector):

    def get_probes(self):
        return ProbeRequest(country_code=self.identifier, return_objects=True)


class Event(object):

    TYPES = ("connect", "disconnect")

    def __init__(self):

        self.start_time = None
        self.stop_time = None
        self.probes = []
        self.type = None

    @staticmethod
    def get_raw_data(probes, t=None):

        t = datetime.utcnow()
        if not t:
            t = datetime.utcnow()

        return AtlasResultsRequest(
            msm_id=7000,
            start=(t - relativedelta(days=1)),
            stop=(t + relativedelta(days=1)),
            probe_ids=[p.id for p in probes]
        ).create()[1]

    def get(self):
        pass
