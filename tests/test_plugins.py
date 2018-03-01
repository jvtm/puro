import json

import pytest

from puro.plugins import Registry


@pytest.fixture(name="reg")
def fixture_registry():
    return Registry()


def test_simple_load(reg: Registry):
    name = reg.load_class("collections.OrderedDict")
    assert name == "collections.OrderedDict"
    items = reg.get_instance(name)
    items["first"] = "hello"
    items["second"] = "world"
    assert json.dumps(items) == '{"first": "hello", "second": "world"}'


def test_plugin_name(reg: Registry):
    pytest.importorskip("jsonschema")
    name = reg.load_class("puro.selectors.jsonschema.JSONSchemaSelector")
    assert name == "jsonschema"
    instance = reg.get_instance(name, "instancename", schema={"type": "string"})
    assert instance.check("hello") is True


def test_getitem(reg: Registry):
    from collections import OrderedDict
    reg.load_class("collections.OrderedDict", name="container")
    assert reg["container"] == OrderedDict


def test_override(reg: Registry):
    compare = {"a": 1}

    name1 = reg.load_class("collections.OrderedDict", name="mapping")
    assert name1 == "mapping"
    cls1 = reg.get_class("mapping")
    assert cls1(a=1) == compare
    assert reg.get_instance("mapping", a=1) == compare

    name2 = reg.load_class("collections.UserDict", name="mapping")
    assert name2 == "mapping"
    cls2 = reg.get_class("mapping")
    assert cls2(a=1) == compare
    assert reg.get_instance("mapping", a=1) == compare
    assert cls1 != cls2


def test_subclass_check(reg: Registry):
    from configparser import RawConfigParser
    reg.load_class("configparser.SafeConfigParser", name="parser", base_class=RawConfigParser)
    cparser = reg.get_instance("parser")
    assert hasattr(cparser, "read")

    with pytest.raises(TypeError):
        reg.load_class("collections.OrderedDict", base_class=RawConfigParser)


def test_errors(reg: Registry):
    invalid = [
        "collections.TurboDict",
        "operator.gt",
        "",
        "filter",
        13,
        None,
    ]
    errors = (AttributeError, TypeError, ValueError)
    for mpath in invalid:
        with pytest.raises(errors):
            name = reg.load_class(mpath)
            print(f"Should not get here: {mpath} {name}")
