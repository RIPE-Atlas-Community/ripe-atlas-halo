# ripe-atlas-halo
A heads-up display for your network


Generate a list of events:

```python
probes = Selector.factory("3333").get_probes()
Event.get_raw_data(probes)
```
