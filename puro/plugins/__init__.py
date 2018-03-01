"""
Plugin registry, base classes and related helpers
"""
import importlib
import inspect
import logging


class Registry:
    """Container for loading plugin classes based on configuration values.
    Plugin classes can be referred by `name`, which makes the overall
    configuration a bit more friendly.
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self._plugins = {}

    def load_class(self, mod_path: str, *, name=None, base_class=None):
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

        if name in self._plugins:
            self.log.warning("Overriding plugin %r %r", name, self._plugins[name])

        self._plugins[name] = plugin_class
        self.log.info("Loaded plugin %r %r", name, plugin_class)

        return name

    def __getitem__(self, item):
        return self.get_class(item)

    def get_class(self, name):
        """Return already loaded class"""
        return self._plugins[name]

    def get_instance(self, name, *args, **kwargs):
        """Create instance of already loaded class"""
        return self._plugins[name](*args, **kwargs)


class BasePlugin:   # pylint: disable=too-few-public-methods
    # XXX: this might get ported from old code next
    def __init__(self, name):
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name
