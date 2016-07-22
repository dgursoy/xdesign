#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2016, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2016. UChicago Argonne, LLC. This software was produced       #
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

import numpy as np
import logging

logger = logging.getLogger(__name__)


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['Point',
           'Circle',
           'Line',
           'Beam']


class Point(object):
    """Point in 2-D Cartesian space saf.

    Attributes
    ----------
    x : scalar
    y : scalar
    """

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        """Addition."""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtraction."""
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, c):
        """Scalar multiplication."""
        return Point(c * self.x, c * self.y)

    @property
    def norm(self):
        """Returns the norm of the point."""
        return np.hypot(self.x, self.y)
        self.y = self.x * np.sin(theta) + self.y * np.cos(theta)

    @property
    def list(self):
        """Returns the point's list representation."""
        return [self.x, self.y]

    @property
    def numpy(self):
        """Returns the Numpy representation."""
        return np.array([self.x, self.y])

    def distance(self, point):
        """Returns the distance from a point."""
        return np.hypot(self.x - point.x, self.y - point.y)

    def rotate(self, theta, origin):
        """Rotate point around a point."""
        dx = self.x - origin.x
        dy = self.y - origin.y
        px = dx * np.cos(theta) - dy * np.sin(theta)
        py = dx * np.sin(theta) + dy * np.cos(theta)
        self.x = px + origin.x
        self.y = py + origin.y


class Circle(object):
    """Circle in 2-D Cartesian space.

    Attributes
    ----------
    center : Point
        Center point of the circle.
    radius : scalar, optional
        Radius of the circle.
    """

    def __init__(self, center, radius, value=1):
        self.center = center
        self.radius = float(radius)
        self.value = float(value)

    def __str__(self):
        return "%s, %s, %s" % (self.center, self.radius, self.value)

    def __mul__(self, c):
        """Expand circle."""
        return Circle(self.center, c * self.radius)

    @property
    def equation(self):
        """Returns circle's analytical equation."""
        return "(x-%s)^2 + (y-%s)^2 = %s^2" % (self.center.x, self.center.y, self.radius)

    @property
    def area(self):
        """Returns circle's area."""
        return np.pi * self.radius**2

    @property
    def circumference(self):
        """Returns circle's circumference."""
        return 2 * np.pi * self.radius

    @property
    def diameter(self):
        """Returns circle's diameter."""
        return 2 * self.radius

    def rotate(self, theta, origin):
        """Rotate circle."""
        self.center = rotate(self.center, theta, origin)

    def translate(self, dx, dy):
        """Translate circle."""
        self.center.x += dx
        self.center.y += dy


class Line(object):
    """Line in 2-D Cartesian space.

    It is defined by two distinct points.

    Attributes
    ----------
    p1 : Point
    p2 : Point
    """

    def __init__(self, p1, p2):
        if p1 == p2:
            raise ValueError('Requires two unique points.')
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "%s, %s, %s" % (self.p1, self.p2)

    @property
    def vertical(self):
        """True if line is vertical."""
        if self.p1.x == self.p2.x:
            return True
        else:
            return False

    @property
    def horizontal(self):
        """True if line is horizontal."""
        if self.p1.y == self.p2.y:
            return True
        else:
            return False

    @property
    def slope(self):
        """Returns the slope of the line."""
        if self.vertical:
            return np.inf
        else:
            return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    @property
    def intercept(self):
        """Returns the intercept point with y-axis."""
        if self.vertical:
            return 0.
        else:
            return self.p1.y - self.slope * self.p1.x

    @property
    def equation(self):
        """Returns line equation."""
        if self.vertical:
            return "x = %s" % self.p1.x
        return "y = %sx + %s" % (self.slope, self.intercept)

    @property
    def tangent(self):
        """Returns unit tangent vector."""
        length = self.p1.distance(self.p2)
        dx = (self.p1.x - self.p2.x) / length
        dy = (self.p1.y - self.p2.y) / length
        return Point(dx, dy)

    @property
    def normal(self):
        """Returns unit normal vector."""
        length = self.p1.distance(self.p2)
        dx = (self.p1.x - self.p2.x) / length
        dy = (self.p1.y - self.p2.y) / length
        return Point(-dy, dx)


class Beam(Line):
    """Beam (thick line) in 2-D Cartesian space.

    It is defined by two distinct points.

    Attributes
    ----------
    p1 : Point
    p2 : Point
    size : scalar, optional
        Size of the beam.
    """

    def __init__(self, p1, p2, size=0):
        super(Beam, self).__init__(p1, p2)
        self.size = float(size)

    def __str__(self):
        return super(Beam, self).__str__()

def rotate(point, theta, origin=Point(0, 0)):
    """Rotates a point in counter-clockwise around another point.
    Parameters
    ----------
    point : Point
        An arbitrary point.
    theta : scalar
        Rotation angle in radians.
    origin : Point, optional
        The origin of rotation axis.
    Returns
    -------
    Point
        Rotated point.
    """
    dx = point.x - origin.x
    dy = point.y - origin.y
    px = dx * np.cos(theta) - dy * np.sin(theta)
    py = dx * np.sin(theta) + dy * np.cos(theta)
    return Point(px + origin.x, py + origin.y)


def segment(circle, x):
    """Calculates intersection area of a vertical line segment in a circle.

    Parameters
    ----------
    circle : Circle
    x : scalar
        Intersection of the vertical line with x-axis.

    Returns
    -------
    scalar
        Area of the left region.
    """
    return circle.radius**2 * \
        np.arccos(x / circle.radius) - x * np.sqrt(circle.radius**2 - x**2)


def beamcirc(beam, circle):
    """Intersection area of an infinite beam with a circle.

    Parameters
    ----------
    beam : Beam
    circle : Circle

    Returns
    -------
    scalar
        Area of the intersected region.
    """

    # Passive coordinate transformation.
    _center = rotate(
        point=circle.center,
        theta=-np.arctan(beam.slope),
        origin=Point(0, beam.intercept))

    # Correction if line is vertical to x-axis.
    if beam.vertical:
        dy = beam.p1.x
    else:
        dy = -beam.intercept

    # Calculate the area deending on how the beam intersects the circle.
    p1 = _center.y - beam.size / 2. + dy
    p2 = _center.y + beam.size / 2. + dy
    pmin = min(abs(p1), abs(p2))
    pmax = max(abs(p1), abs(p2))
    if pmin < circle.radius:
        if pmax >= circle.radius:
            if p1 * p2 > 0:
                area = segment(circle, pmin)
            else:
                area = circle.area - segment(circle, pmin)
        elif pmax < circle.radius:
            area = abs(segment(circle, p1) - segment(circle, p2))
    elif p1 * p2 < 0:
        area = circle.area
    else:
        area = 0.
    return area
