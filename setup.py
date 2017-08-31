import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md") as f:
    readme = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ]

setup(
    name = "pypgfplots",
    version = "0.0.1",
    description = "Create simple tikz figure (pgfplots) from python-numpy arrays.",
    long_description = readme,
    packages = [ '' ],
    package_data = {},
    install_requires = [ ],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/",
    license='GPL',
    classifiers=classifiers,
)
