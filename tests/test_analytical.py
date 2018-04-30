"""Tests for analytical module."""

import pytest
from . import tol_check

from uhb import analytical

test_inputs = {"D": 0.1683, "t": 0.011, "t_coat": 0.0024}

def test_required_download():
    assert tol_check(
        analytical.required_download(0.5, 207e9, 1.689e-5, 786019, 193.34), 3873
    )