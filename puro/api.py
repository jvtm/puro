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
import logging
import uuid

from .plugins import BasePlugin, Registry


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
        "puro.selectors.jsonschema.JSONSchemaSelector",
        "puro.selectors.kmatch.KmatchSelector",
        "puro.plugins.jmespath.JMESPath",
    )

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.registry = Registry()
        for mod_path in self.DEFAULT_PLUGINS:
            try:
                self.registry.load_class(mod_path, base_class=BasePlugin)
            except ImportError as ex:
                self.log.info("Failed to load plugin class %r: %s", mod_path, ex)
