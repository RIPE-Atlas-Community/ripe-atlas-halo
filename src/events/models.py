from datetime import datetime, timedelta
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


class Outages(object):
    """
    The Outages class here refers to something that finds outages of
    interest. Basically an "outage" is defined as having too many RIPE
    Atlas probes disconnect in a short time.

    We pass in:

    * start_time: when to start looking for events, datetime-formatted
    * stop_time: last time to look for events, datetime-formatted
    * probes: iterable with list of probe objects
    * threshold_interval: number of seconds to check for events in
    * threshold_p: portion of probes to trigger the event [0, 1]
    """
    def __init__(self, start_time, stop_time, probes,
                 threshold_interval, threshold_p):
        self.start_time = start_time
        self.stop_time = stop_time
        self.probe_ids = [p.id for p in list(probes)]
        self.threshold_interval = relativedelta(seconds=threshold_interval)
        self.threshold_p = threshold_p

    def _get_connect_and_disconnect_events(self):
        """
        Return all of the connect and disconnect events from Atlas.

        These events are a list of dict, each of which looks like 
        this:

            {'asn': '3292',
             'controller': 'ctr-nue16',
             'event': 'connect',
             'msm_id': 7000,
             'prb_id': 22964,
             'prefix': '83.88.0.0/13',
             'timestamp': 1463848675,
             'type': 'connection'},

        This list is sorted by timestamp.
        """
        results = AtlasResultsRequest(
            # 7000 is the undocumented magical measurement ID which 
            # returns the connect & disconnect events
            msm_id = 7000,
            start = self.start_time,
            stop = self.stop_time,
            probe_ids = self.probe_ids
        ).create()[1]
        return sorted(results, key=lambda x: x['timestamp'])

    def get(self):
        """
        Look through our disconnect events and find when we have a
        noteworthy outage event.

        We can figure out the number of probes that indicates this.
        That is the (total number of probes) * (alert percentage).

        We then look for any time period that has that many disconnect
        events from different probes. We use an inefficient algorithm
        for this, because there are typically only a few such events.
        (An hour time slice in all of Denmark had 8 in a quick test.)

        Returns a sorted list of time ranges, along with a set of
        probes failing during each range. The list covers the whole
        time period, so the set of probes failing for any given time
        may be empty. Like this:

        [ 
          { 'start_time': 123,
            'stop_time': 456, 
            'probe_ids': set([555, 666, 777]) },
          { 'start_time': 457,
            'stop_time': 999,
            'probe_ids': set() },
          { 'start_time': 1000,
            'stop_time': 1001,
            'probe_ids': set([111, 555, 666, 777] },
        ]
        """
        failed_level = int(len(self.probe_ids) * self.threshold_p)

        # search through our events and find disconnect events 
        # that are within the time period
        all_evts = self._get_connect_and_disconnect_events()
        unpacked_outages = []
        for n, evt in enumerate(all_evts):
            # use a set to insure that we only track each probe
            # that disconnects once
            down_prb_ids = set([evt['prb_id']])

            # start time is from this event, stop time may change
            # if we find other events in this time period
            start_time = datetime.fromtimestamp(evt['timestamp'])
            stop_time = datetime.fromtimestamp(evt['timestamp'])

            # check all events after this one that are in this 
            # time window
            time_limit = start_time + self.threshold_interval
            for check_evt in all_evts[n+1:]:
                when = datetime.fromtimestamp(check_evt['timestamp'])
                if when > time_limit:
                    break
                if check_evt['event'] == 'disconnect':
                    down_prb_ids.add(check_evt['prb_id'])
                    stop_time = when
            possible_outage = {
                'start_time': start_time,
                'stop_time': stop_time,
                'probe_ids': down_prb_ids,
            }
            unpacked_outages.append(possible_outage)

        # now that we have all possible events we go through them 
        # collecting events that have overlapping times
        packed_outages = []
        for outage in unpacked_outages:
            # check that there are enough probes in this interval to 
            # count as a failure
            num_failed = len(outage['probe_ids'])
            if packed_outages:
                prev = packed_outages[-1]
                if prev['stop_time'] >= outage['start_time']:
                    # merging with the previous outage, if time overlaps
                    prev['stop_time'] = outage['stop_time']
                    new_ids = prev['probe_ids'].union(outage['probe_ids'])
                    prev['probe_ids'] = new_ids
                elif num_failed >= failed_level:
                    # if we have enough probes to count as an outage, add
                    packed_outages.append(outage)
            elif num_failed >= failed_level:
                # if we have enough probes to count as an outage, add
                packed_outages = [outage]

        # finally, go through and add ranges for non-outage times
        all_outages = []
        when = self.start_time
        while when < self.stop_time:
            if packed_outages:
                outage = packed_outages[0]
                packed_outages = packed_outages[1:]
                next_start = outage['start_time']
                if next_start > when:
                    non_outage = {
                        'start_time': when,
                        'stop_time': next_start + timedelta(seconds=-1),
                        'probe_ids': set(),
                    }
                    all_outages.append(non_outage)
                all_outages.append(outage)
                when = outage['stop_time'] + timedelta(seconds=1)
            else:
                non_outage = {
                    'start_time': when,
                    'stop_time': self.stop_time,
                    'probe_ids': set(),
                }
                all_outages.append(non_outage)
                when = self.stop_time + timedelta(seconds=1)
                
        return all_outages

#def test():
#    start = datetime.utcnow() - relativedelta(days=1)
##    start = datetime.utcnow() - relativedelta(hours=1)
#    stop = datetime.utcnow()
#    probes = list(Selector.factory("dk").get_probes())
#    print("There are %d probes" % len(list(probes)))
#    ev = Outages(start, stop, probes, 900, 0.01)
#    return ev.get()
