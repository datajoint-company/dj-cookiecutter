"""An example test file that loads the dj_config fixture from conftest.py."""


def test_dj_config_exists(dj_config):
    assert dj_config is not None
