"""Tests for general module."""

import pytest

from uhb import general

tol = 0.001

test_inputs = {"D": 0.1683, "t": 0.011, "t_coat": 0.0024}


def test_area_of_steel():
    expected = 0.005436
    assert (
        abs(general.area_of_steel(test_inputs["D"], test_inputs["t"]) - expected)
        <= tol * expected
    )


def test_area_of_coating():
    expected = 0.001287
    assert (
        abs(general.area_of_coating(test_inputs["D"], test_inputs["t_coat"]) - expected)
        <= tol * expected
    )


def test_internal_area():
    expected = 0.016810
    assert (
        abs(general.internal_area(test_inputs["D"], test_inputs["t"]) - expected)
        <= tol * expected
    )


def test_total_area():
    expected = 0.023533
    assert (
        abs(general.total_area(test_inputs["D"], test_inputs["t_coat"]) - expected)
        <= tol * expected
    )
