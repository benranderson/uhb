"""Tests for general module."""

import pytest
from . import tol_check

from uhb import general

test_inputs = {"D": 0.1683, "t": 0.011, "t_coat": 0.0024}


def test_total_outside_diameter():
    assert tol_check(
        general.total_outside_diameter(test_inputs["D"], test_inputs["t_coat"]), 0.1731
    )


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
    assert tol_check(general.total_area(0.1731), 0.023533)


def test_second_moment_of_area():
    assert tol_check(
        general.second_moment_of_area(test_inputs["D"], test_inputs["t"]), 1.689e-5
    )


def test_effective_axial_force():
    A_i = general.internal_area(test_inputs["D"], test_inputs["t"])
    A_s = general.area_of_steel(test_inputs["D"], test_inputs["t"])
    assert tol_check(
        abs(general.effective_axial_force(0, 1.9e7, A_i, 0.3, A_s, 207e9, 11.7e-6, 50)),
        786019,
    )


def test_submerged_weight():
    assert tol_check(
        general.submerged_weight(
            test_inputs["D"],
            test_inputs["t"],
            test_inputs["t_coat"],
            7850,
            900,
            0,
            1025,
            9.81,
        ),
        193.34,
    )
