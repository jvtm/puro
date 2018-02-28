"""
Selectors are used on main program flow to decide whether or not to
descend into the given (sub-)tree of actions.
"""
from puro.plugins import BasePlugin


class Selector(BasePlugin):
    def check(self, item):
        """Check if single item matches the configured schema, restrictions.

        Usually `item` is dictionary, but other basic types possible too
        Note: task/feed/service context are intentionally not available here.

        For now any logic that needs to remember anything, access external data
        stores, etc should be implemented as Action instead
        """
        raise NotImplementedError()
