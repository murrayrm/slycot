#!/usr/bin/env python
from __future__ import division, print_function
import glob
import os
import sys
import sysconfig

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('slycot', parent_package, top_path)

    # can disable building extension to test packaging
    build_fortran = True

    if build_fortran:
        fortran_sources = glob.glob(
            os.path.join('slycot', 'src', '*.f'))
    else:
        print('WARNING FORTRAN BUILD DISABLED')
        fortran_sources = []

    f2py_sources = ['src/_wrapper.pyf']

    pyver = sysconfig.get_config_var('VERSION')

    if sys.platform == 'win32':
        liblist = ['liblapack', 'libblas']
    else:
        # this is needed on Py 3.x, and fails on Py 2.7
        try:
            abiflags = sys.abiflags
        except AttributeError:
            abiflags = ''
        liblist = ['lapack', 'blas', 'python'+pyver+abiflags]

    config.add_extension(
        name='_wrapper',
        libraries=liblist,
        sources=fortran_sources + f2py_sources)

    config.make_config_py()  # installs __config__.py

    config.add_subpackage('tests')

    return config

if __name__ == '__main__':
    print('This is the wrong setup.py file to run')
