"""
Selector using kmatch

http://kmatch.readthedocs.io
https://pypi.python.org/pypi/kmatch

This is a simple top level matching for dictionaries. It does have notion
of boolean operators, integer comparisons, exact matching and regular
expressions. This might be usable on cases where a full-blown JSON
schema matcher is too much. Also serves as an example how to create
your own selectors.
"""
import json

from kmatch import K

from . import Selector


class KmatchSelector(Selector):
    plugin_name = "kmatch"

    def __init__(self, name, *, kmatch=None, kmatch_path=None, suppress_key_errors=True):
        super().__init__(name)

        if kmatch is None:
            with open(kmatch_path) as fob:
                kmatch = json.load(fob)

        self.kmatch = K(kmatch, suppress_key_errors=suppress_key_errors)

    def check(self, item):
        try:
            return self.kmatch.match(item)
        except (KeyError, TypeError, ValueError):
            # trying to match against non-dictionary, missing keys, unexpected value types, ...
            return False
