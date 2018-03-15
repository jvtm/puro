from puro.api import Flow


def test_load_defaults():
    # Nothing real yet... waiting for config helper cleanups
    config = {
        "plugins": [],
        "actions": [],
        "service_plugins": [],      # FIXME: better name
        "queue_size": 10,
    }
    flow = Flow(config)
    assert flow.registry
