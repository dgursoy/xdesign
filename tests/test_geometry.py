#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2016, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2015. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from phantom.geometry import *
from phantom.geometry import beamcirc
from numpy.testing import assert_allclose, assert_raises
import numpy as np


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'


# Nonintersecting beams

def test_beamcirc_nonintersecting_top():
    circ = Circle(Point(0, 3), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 0., rtol=1e-6)


def test_beamcirc_nonintersecting_bottom():
    circ = Circle(Point(0, -3), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 0., rtol=1e-6)


# Partial intersections

def test_beamcirc_intersecting_partially_from_top_outside_center():
    circ = Circle(Point(0, 1.5), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 0.614184849304, rtol=1e-6)


def test_beamcirc_intersecting_partially_from_bottom_outside_center():
    circ = Circle(Point(0, -1.5), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 0.614184849304, rtol=1e-6)


def test_beamcirc_intersecting_partially_from_top_inside_center():
    circ = Circle(Point(0, 0.5), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 2.52740780429, rtol=1e-6)


def test_beamcirc_intersecting_partially_from_bottom_inside_center():
    circ = Circle(Point(0, -0.5), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 2.52740780429, rtol=1e-6)


# Full intersections

def test_beamcirc_intersecting_fully_from_top_outside_center():
    circ = Circle(Point(0, 1.5), 3)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 10.0257253792, rtol=1e-6)


def test_beamcirc_intersecting_fully_from_bottom_outside_center():
    circ = Circle(Point(0, -1.5), 3)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 10.0257253792, rtol=1e-6)


def test_beamcirc_intersecting_fully_from_top_inside_center():
    circ = Circle(Point(0, 0.5), 3)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 11.5955559562, rtol=1e-6)


def test_beamcirc_intersecting_fully_from_bottom_inside_center():
    circ = Circle(Point(0, -0.5), 3)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 11.5955559562, rtol=1e-6)


def test_beamcirc_intersecting_fully():
    circ = Circle(Point(0, 0), 1)
    beam = Beam(Point(-2, 0), Point(2, 0), 2)
    assert_allclose(beamcirc(beam, circ), 3.14159265359, rtol=1e-6)


# Vertical intersection.

def test_beamcirc_vertical_intersection():
    circ = Circle(Point(0, 0), 1)
    beam = Beam(Point(-1, -1), Point(1, 1), 1)
    assert_allclose(beamcirc(beam, circ), 1.91322295498, rtol=1e-6)


# Line

def test_Line_slope_vertical():
    line = Line(Point(0, -1), Point(0, 1))
    assert_allclose(line.slope, np.inf, rtol=1e-6)


def test_Line_intercept_vertical():
    line = Line(Point(0, -1), Point(0, 1))
    assert_allclose(line.intercept, 0, rtol=1e-6)


def test_Line_slope():
    line = Line(Point(-1, 0), Point(1, 2))
    assert_allclose(line.slope, 1, rtol=1e-6)


def test_Line_intercept():
    line = Line(Point(-1, 0), Point(1, 2))
    assert_allclose(line.intercept, 1, rtol=1e-6)


def test_Line_same_points():
    assert_raises(ValueError, Line, Point(1, 2), Point(1, 2))


# Circle

def test_Circle_area():
    circle = Circle(Point(0, 0), 1)
    assert_allclose(circle.area, 3.14159265359, rtol=1e-6)


if __name__ == '__main__':
    import nose
    nose.runmodule(exit=False)