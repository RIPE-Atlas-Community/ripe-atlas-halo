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
