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

from .plugins import BasePlugin, Registry


class Flow:
    DEFAULT_PLUGINS = (
        "puro.selectors.jsonschema.JSONSchemaSelector",
        "puro.selectors.kmatch.KmatchSelector",
    )

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.registry = Registry()
        for mod_path in self.DEFAULT_PLUGINS:
            try:
                self.registry.load_class(mod_path, base_class=BasePlugin)
            except ImportError as ex:
                self.log.info("Failed to load plugin class %r: %s", mod_path, ex)
