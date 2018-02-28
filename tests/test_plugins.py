import json

import pytest

from puro.plugins import Registry


@pytest.fixture(name="reg")
def fixture_registry():
    return Registry()


def test_simple_load(reg):
    cls = reg.load_class("collections.OrderedDict")
    items = cls()
    items["first"] = "hello"
    items["second"] = "world"
    assert json.dumps(items) == '{"first": "hello", "second": "world"}'


def test_override(reg):
    compare = {"a": 1}

    cls1 = reg.load_class("collections.OrderedDict", name="mapping")
    assert reg.get_class("mapping") == cls1
    assert reg.get_instance("mapping", a=1) == compare
    assert cls1(a=1) == compare

    cls2 = reg.load_class("collections.UserDict", name="mapping")
    assert reg.get_class("mapping") == cls2
    assert reg.get_instance("mapping", a=1) == compare
    assert cls2(a=1) == compare


def test_subclass_check(reg):
    from configparser import RawConfigParser
    reg.load_class("configparser.SafeConfigParser", name="parser", base_class=RawConfigParser)
    cparser = reg.get_instance("parser")
    assert hasattr(cparser, "read")

    with pytest.raises(TypeError):
        reg.load_class("collections.OrderedDict", base_class=RawConfigParser)


def test_errors(reg):
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
            cls = reg.load_class(mpath)
            print(f"Should not get here: {mpath} {cls}")
