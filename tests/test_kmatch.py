import json
import time

from puro.plugins.kmatch import KmatchSelector


def test_simple():
    now = int(time.time())
    item = {
        "version": 2,
        "username": "nobody",
        "entry": {
            "timestamp": now,
            "message": "Hello World",
        }
    }
    kpat = [
        "&", [
            [">", "version", 0],
            ["=~", "username", "^[a-z0-9]{1,8}$"],
        ]
    ]
    selector = KmatchSelector("test", kmatch=kpat)
    assert selector.check(item)
    assert not selector.check({})
    assert not selector.check({"version": 3})
    assert not selector.check({"version": 3, "username": "<blink>"})
    assert not selector.check("this should not raise anything")


def test_from_file(tmpdir):
    kfile = tmpdir.join("filter.txt")
    kfile.write(json.dumps(["==", "hello", "world"]))
    selector = KmatchSelector("test", kmatch_path=kfile.strpath)
    assert selector.check({"hello": "world", "version": 1})
    assert not selector.check({"hello": "mars", "version": 1})
