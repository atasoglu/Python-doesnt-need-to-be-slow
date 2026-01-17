#!/usr/bin/env python3
"""
Setup script to compile mypyc_impl.py using mypyc
"""

from mypyc.build import mypycify
from setuptools import setup

setup(
    name="nbody_mypyc",
    ext_modules=mypycify([
        "mypyc_impl.py"
    ]),
    zip_safe=False,
)