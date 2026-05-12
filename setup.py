from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='High-Frequency Engine Core',
    ext_modules=cythonize("core/fast_matching_engine.pyx", compiler_directives={'language_level': "3"}),
    include_dirs=[numpy.get_include()]
)
