import json

from puro.selectors.jsonschema import JSONSchemaSelector

SCHEMA_SIMPLE_WITH_VERSION = {
    "type": "object",
    "minProperties": 2,
    "properties": {
        "version": {
            "type": "integer",
            "minimum": 1,
        },
    },
    "required": ["version"],
}


def test_simple_schema():
    validator = JSONSchemaSelector("simple", schema=SCHEMA_SIMPLE_WITH_VERSION)
    assert validator.check({"version": 1, "hello": "world"})
    assert not validator.check({"version": 1})
    assert not validator.check({"hello": "world"})
    assert not validator.check({"version": None})
    assert not validator.check(None)
    assert not validator.check("bogus")
    assert not validator.check({})
    assert not validator.check(object())


def test_schema_from_file(tmpdir):
    jfile = tmpdir.join("simpleschema.json")
    jfile.write(json.dumps(SCHEMA_SIMPLE_WITH_VERSION))
    validator = JSONSchemaSelector("simple", schema_path=jfile.strpath)
    assert validator.check({"version": 1, "foo": "bar", "magic": 42})
