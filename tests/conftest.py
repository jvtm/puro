import pytest

from puro.plugins import BasePlugin, Registry


@pytest.fixture(name="registry")
def fixture_registry(request):
    reg = Registry()
    marker = request.node.get_marker("puro_plugins")
    if marker:
        for mod_path in marker.args:
            try:
                reg.load_class(mod_path, base_class=BasePlugin)
            except ModuleNotFoundError as ex:
                # Can't import, eg. missing dependency library -> SKIP
                pytest.skip(f"Test requires {mod_path!r}: {ex}")
            except (AttributeError, TypeError, ValueError) as ex:
                # Invalid module path -> FAIL
                pytest.fail(f"Invalid plugin path {mod_path!r}: {ex}")
    return reg
