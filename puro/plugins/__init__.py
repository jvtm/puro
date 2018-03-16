"""
Plugin registry, base classes and related helpers
"""
import importlib
import inspect
import logging
from typing import Optional, Type

from ..errors import StopProcessing


class Registry:
    """Container for loading plugin classes based on configuration values.
    Plugin classes can be referred by `name`, which makes the overall
    configuration a bit more friendly.
    """
    def __init__(self):
        self._plugins = {}

    def load_class(self, mod_path: str, *, name: Optional[str] = None, base_class: Optional[Type] = None) -> str:
        """ Load a class into the registry

        If name is not given, `plugin_name` class variable is checked from
        the loaded class. If that is missing, full module path is used.

        :param mod_path: full module path including the class name
        :param name: override plugin name
        :param base_class: optional sub-class check
        :return: loaded plugin name (to be used with other methods)
        """
        mod_name, _, class_name = mod_path.rpartition(".")
        module = importlib.import_module(mod_name)
        plugin_class = getattr(module, class_name)
        if not inspect.isclass(plugin_class):
            raise TypeError(f"{mod_path!r} is not pointing to a class")
        if base_class is not None and not issubclass(plugin_class, base_class):
            raise TypeError(f"{mod_path!r} {plugin_class} is not sub-class of {base_class}")

        if name is None:
            name = getattr(plugin_class, "plugin_name", mod_path)

        self._plugins[name] = plugin_class
        return name

    # def add_class(self, name: str, plugin_class: Type, base_class: Optional[Type]):
    #    """Add class by name"""
    #    ...for adding already existing class more directly, eg. known internal classes, tests, ...
    #   if adding this, then maybe also __setitem__() should be added
    #   move the checks here. almost same signature as above, just plugin_class instead of name

    def __getitem__(self, item):
        return self.get_class(item)

    def get_class(self, plugin_name: str):
        """Return already loaded class"""
        return self._plugins[plugin_name]

    def get_instance(self, plugin_name: str, *args, **kwargs):
        """Create instance of already loaded class"""
        return self._plugins[plugin_name](*args, **kwargs)


class BasePlugin:   # pylint: disable=too-few-public-methods
    def __init__(self, name: str):
        # perhaps logger should be the name, with a prefix...
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name


class Action(BasePlugin):
    async def __call__(self, item):
        raise NotImplementedError()


class Selector(Action):
    def check(self, value):
        """Check if single item matches the configured schema, restrictions.

        Usually `value` is dictionary, but other basic types possible too
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


class ServicePlugin(BasePlugin):
    """Base class for service plugins
    Instantiated once, and reachable via service context
    Useful for DB connections, global state objects, statistics etc
    """
    async def initialize(self):
        """Initialize service plugin"""
        # This is the place to do connection, pool, etc creation,
        # especially if those are coroutines themselves
        # TODO: might add loop=None keyword argument, if we ever want to use custom loop
        pass
