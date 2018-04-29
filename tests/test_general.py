"""Tests for general module."""

import pytest
from . import tol_check

from uhb import general

test_inputs = {"D": 0.1683, "t": 0.011, "t_coat": 0.0024}


def test_area_of_steel():
    assert tol_check(
        general.area_of_steel(test_inputs["D"], test_inputs["t"]), 0.005436
    )


def test_area_of_coating():
    assert tol_check(
        general.area_of_coating(test_inputs["D"], test_inputs["t_coat"]), 0.001287
    )


def test_internal_area():
    assert tol_check(
        general.internal_area(test_inputs["D"], test_inputs["t"]), 0.016810
    )


def test_total_area():
    assert tol_check(
        general.total_area(test_inputs["D"], test_inputs["t_coat"]), 0.023533
    )
