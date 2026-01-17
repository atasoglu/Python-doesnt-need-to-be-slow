#!/usr/bin/env python3
"""
Setup script to compile baseline.py using mypyc
"""

from mypyc.build import mypycify
from setuptools import setup

setup(
    name="nbody_mypyc",
    ext_modules=mypycify([
        "baseline.py"
    ]),
    zip_safe=False,
)