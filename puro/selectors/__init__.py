"""
Selectors are used on main program flow to decide whether or not to
descend into the given (sub-)tree of actions.
"""
from ..errors import StopProcessing
from ..plugins import Action


class Selector(Action):
    def check(self, value):
        """Check if single item matches the configured schema, restrictions.

        Usually `item` is dictionary, but other basic types possible too
        Note: task/feed/service context are intentionally not available here.

        For now any logic that needs to remember anything, access external data
        stores, etc should be implemented as Action instead

        For now, this SHOULD NOT raise any ValueErrors, KeyErrors etc.
        So, depending on the used helpers, catch whatever it might throw at you.
        """
        raise NotImplementedError()

    async def __call__(self, item):
        if not self.check(item.value):
            raise StopProcessing()
