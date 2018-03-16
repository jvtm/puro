"""
Unit-tests for basic Puro plugin loading logic.

Might include some really simple test for the plugins themselves, but more comprehensive
tests for internal plugin logic should go into `test_<plugin_name>.py` instead.

Additionally, combinations of multiple plugins should go into `test_flow.py`.

To autoload a plugin by its module path (and use it by its default name),
use `@pytest.mark.puro_plugins("plugin.path.here.Plugin") decorator in combination
with `registry` fixture.

TODO: will get re-organized, so that this test module contains only core
plugin logic, class structure etc.
"""
import json

import pytest

from puro.api import Task
from puro.plugins import Registry


def test_simple_load(registry: Registry):
    name = registry.load_class("collections.OrderedDict")
    assert name == "collections.OrderedDict"
    items = registry.get_instance(name)
    items["first"] = "hello"
    items["second"] = "world"
    assert json.dumps(items) == '{"first": "hello", "second": "world"}'


def test_plugin_name(registry: Registry):
    pytest.importorskip("jsonschema")
    name = registry.load_class("puro.plugins.jsonschema.JSONSchemaSelector")
    assert name == "jsonschema"
    instance = registry.get_instance(name, "instancename", schema={"type": "string"})
    assert instance.check("hello") is True


@pytest.mark.asyncio
@pytest.mark.puro_plugins("puro.plugins.jmespath.JMESPath")
async def test_jmespath_action(registry: Registry):
    action = registry.get_instance("jmespath", "only_version", expression="{version: version}")
    task = Task({"version": 1, "value": "something-complex-here"})
    await action(task)
    assert task.value == {"version": 1}


def test_getitem(registry: Registry):
    from collections import OrderedDict
    registry.load_class("collections.OrderedDict", name="container")
    assert registry["container"] == OrderedDict


def test_override(registry: Registry):
    compare = {"a": 1}

    name1 = registry.load_class("collections.OrderedDict", name="mapping")
    assert name1 == "mapping"
    cls1 = registry.get_class("mapping")
    assert cls1(a=1) == compare
    assert registry.get_instance("mapping", a=1) == compare

    name2 = registry.load_class("collections.UserDict", name="mapping")
    assert name2 == "mapping"
    cls2 = registry.get_class("mapping")
    assert cls2(a=1) == compare
    assert registry.get_instance("mapping", a=1) == compare
    assert cls1 != cls2


def test_subclass_check(registry: Registry):
    from configparser import RawConfigParser
    registry.load_class("configparser.SafeConfigParser", name="parser", base_class=RawConfigParser)
    cparser = registry.get_instance("parser")
    assert hasattr(cparser, "read")

    with pytest.raises(TypeError):
        registry.load_class("collections.OrderedDict", base_class=RawConfigParser)


def test_add_class(registry: Registry):
    registry.add_class("notfound", FileNotFoundError, base_class=OSError)
    with pytest.raises(FileNotFoundError):
        raise registry.get_instance("notfound", "Missing")


def test_errors(registry: Registry):
    invalid = [
        "collections.TurboDict",
        "operator.gt",
        "",
        ".",
        "filter",
        13,
        None,
    ]
    errors = (AttributeError, TypeError, ValueError)
    for mpath in invalid:
        with pytest.raises(errors):
            name = registry.load_class(mpath)
            print(f"Should not get here: {mpath} {name}")
