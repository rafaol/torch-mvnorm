from setuptools import find_packages
from distutils.core import setup

# Make sure numpy and Cython get installed first.
from setuptools import dist
dist.Distribution().fetch_build_eggs(['Cython>=0.29.15', 'numpy>=1.18.0'])

from numpy import get_include


setup(
    name = 'mvnorm',
    version="0.1",
    packages=find_packages(),
    include_dirs = [get_include()]
    )
