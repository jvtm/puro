"""
Selector using JSON Schema

JSON Schema:
* http://json-schema.org/
* http://json-schema.org/latest/json-schema-validation.html

Python library:
* https://python-jsonschema.readthedocs.io
* https://pypi.python.org/pypi/jsonschema
* https://github.com/Julian/jsonschema

Note: even when the name has "JSON" in it, the library is used
against Python objects (usually dictionaries, but other basic types
are possible too, eg. direct string mathcing).

Later on different draft versions, extensions etc might get supported,
but this covers 98% of real life use-cases already.

Optional "format checkers" should work too, if you have the necessary
libraries installed. Remember that they are usually _optional_.
See https://python-jsonschema.readthedocs.io/en/latest/validate/#validating-formats
"""
import json

from jsonschema import Draft4Validator

from . import Selector


class JSONSchemaSelector(Selector):
    plugin_name = "jsonschema"

    def __init__(self, name, *, schema=None, schema_path=None):
        super().__init__(name)

        if schema is None:
            with open(schema_path) as fob:
                schema = json.load(fob)

        # Validating schema only once, `jsonschema.validate()` helper
        # would do the same thing on each call
        Draft4Validator.check_schema(schema)
        self.validator = Draft4Validator(schema)

    def check(self, value):
        return self.validator.is_valid(value)
