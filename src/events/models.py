from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.cache import cache
from django_countries import countries

from ripe.atlas.cousteau import AtlasResultsRequest, ProbeRequest


class Selector(object):

    LOOKUP = None

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

    def get_probes(self):

        cache_key = "probes-{}".format(self.identifier)

        r = cache.get(cache_key)
        if r is not None:
            return r

        cache.set(cache_key, ProbeRequest(**{
            self.LOOKUP: self.identifier,
            "return_objects": True
        }), 60 * 15)

        return self.get_probes()


class AsSelector(Selector):

    LOOKUP = "asn"

    def __init__(self, string):
        Selector.__init__(self, string)
        self.identifier = int(self.identifier)


class PrefixSelector(Selector):

    LOOKUP = "prefix"


class CountrySelector(Selector):

    LOOKUP = "country_code"


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
