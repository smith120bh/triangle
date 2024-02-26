Triangle
--------

[![Build Status](https://github.com/smith120bh/triangle/actions/workflows/wheels.yml/badge.svg?branch=master)](https://github.com/smith120bh/triangle/actions/workflows/wheels.yml)
<!-- [![Version Status](https://img.shields.io/pypi/v/triangle.svg)](https://pypi.python.org/pypi/triangle/)
[![Downloads](https://img.shields.io/pypi/dm/triangle.svg)](https://pypi.python.org/pypi/triangle/) -->

*Triangle* is a python wrapper around Jonathan Richard Shewchuk's two-dimensional quality mesh generator and delaunay triangulator library, available [here](https://www.cs.cmu.edu/~quake/triangle.html). This implementation utilizes [Cython](https://cython.org) to wrap the C API as closely as possible. It is based upon work by Drufat ([original Github](https://github.com/drufat/triangle) and [original Documentation](https://rufat.be/triangle)).

This version modernises package structure, adds linting and type checking, and most importantly, adds fully-functional automated builds for all platforms.
