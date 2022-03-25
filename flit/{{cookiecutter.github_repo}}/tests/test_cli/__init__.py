"""fixture example

See: https://docs.pytest.org/en/6.2.x/fixture.html
"""

import os
from pathlib import Path

import datajoint as dj
import pytest


@pytest.fixture
def dj_config():
    if Path("./dj_local_conf.json").exists():
        dj.config.load("./dj_local_conf.json")

    dj.config["safemode"] = False
    dj.config["loglevel"] = "DEBUG"

    yield dj.config
