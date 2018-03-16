"""
Copyright 2018 Jyrki Muukkonen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio
import logging
import uuid
from copy import deepcopy

from .plugins import BasePlugin, Registry, ServicePlugin


class Task:
    def __init__(self, value, task_id=None, item_context=None, service_context=None):
        if task_id is None:
            task_id = uuid.uuid4()
        self.task_id = task_id                      # perhaps this should be in item context, keeping track of the orig
        self.value = value                          # whatever our value is
        self.item_context = item_context            # information about _this_ task... not sure what yet
        self.service_context = service_context      # for holding service info, stats + service plugins
        # TODO: timestamps here?

    def __repr__(self):
        return f"<Task {self.task_id}>"

    def copy(self):
        # TODO: return a copy of self, for passing into parallel processing
        return self


class Flow:
    DEFAULT_PLUGINS = (
        "puro.plugins.jsonschema.JSONSchemaSelector",
        "puro.plugins.kmatch.KmatchSelector",
        "puro.plugins.jmespath.JMESPath",
    )

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(self.__class__.__name__)

        # Load plugin classes
        self.registry = Registry()
        self.load_plugins([{"class": x} for x in self.DEFAULT_PLUGINS], ignore_import_errors=True)
        self.load_plugins(config["plugins"])

        # Load actions, service plugins etc (instances of plugin classes)
        self.actions = self.load_instances(config["actions"])
        self.service_plugins = self.load_instances(config["service_plugins"])

        # TODO: load rules
        # self.root = Node()

        # TODO: assign readers/producers

        self.queue = asyncio.Queue(maxsize=config["queue_size"])
        self.running = None

    def load_plugins(self, plugins, ignore_import_errors=False):
        catch = ModuleNotFoundError if ignore_import_errors else ()
        for plugin in plugins:
            name = plugin.get("name")
            mod_path = plugin.get("class")
            try:
                self.registry.load_class(mod_path, name=name, base_class=BasePlugin)
            except catch as ex:
                self.log.info("Failed to load plugin class %r %s", plugin, ex)

    def load_instances(self, items):
        loaded = {}
        for item in items:
            name = item["name"]
            kwargs = deepcopy(item)
            plugin_name = kwargs.pop("plugin")
            loaded[name] = self.registry.get_instance(plugin_name, **kwargs)
            self.log.info("Loaded instance %s %s %r", name, plugin_name, loaded[name])
        return loaded

    async def initialize(self):
        """Initialize asyncio related service parts, including service plugins"""
        for name, plugin in self.service_plugins.items():
            if isinstance(plugin, ServicePlugin):
                self.log.info("Initializing %r", name)
                await plugin.initialize()

    def create_task(self, obj) -> Task:
        # TODO: item context, stats, ...
        return Task(obj, service_context=self.service_plugins)

    async def enque(self, item):
        if not isinstance(item, Task):
            item = self.create_task(item)
        await self.queue.put(item)
        return item
