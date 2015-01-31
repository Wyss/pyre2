#!/usr/bin/env python
import sys
import os
import re
from distutils.core import setup, Extension
from os import makedirs
import shutil

DESCRIPTION = "Python wrapper for Google's RE2 using Cython"

DISTNAME = 're2'
LICENSE = 'New BSD License'
EMAIL = "nick.conway@wyss.harvard.edu"
URL = ""
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Cython',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

from distutils.core import setup, Extension
from distutils.command import install_lib, sdist, build_ext
# from Cython.Distutils import Extension
from Cython.Build import cythonize
import os
from os.path import join as pjoin
import sys
import shutil


PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')
RE2_SRC_PATH =          pjoin(PACKAGE_PATH, 're2_cpp')
RE2_INSTALL_PATH =      pjoin(MODULE_PATH, 'src', 're2_cpp')

def get_long_description():
    with open(pjoin(PACKAGE_PATH, "README.rst")) as readme_f:
        readme = readme_f.read()
    return readme

def get_authors():
    author_re = re.compile(r'^\s*(.*?)\s+<.*?\@.*?>', re.M)
    with open(pjoin(PACKAGE_PATH, "AUTHORS")) as authors_f:
        authors = [match.group(1) for match in author_re.finditer(authors_f.read())]
    return ', '.join(authors)

# see:
# http://stackoverflow.com/questions/19123623/python-runtime-library-dirs-doesnt-work-on-mac
RE2_LIB_PATH = pjoin(RE2_SRC_PATH, "lib")

# re2_ext = Extension( "re2._re2",
#         sources=['re2/_re2.pyx'],
#         language="c++",
#         include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
#         libraries=["re2_dyn"],
#         library_dirs=[RE2_LIB_PATH],
#         # runtime_library_dirs=[RE2_LIB_PATH],
#         # extra_objects=[pjoin(RE2_LIB_PATH, 'libre2_static.a')],
#         extra_compile_args=['-Wno-unused-function'],
#     )

re2_cpp_src = [
    pjoin("util", "arena.cc"),
    pjoin("util", "hash.cc"),
    pjoin("util", "rune.cc"),
    pjoin("util", "stringpiece.cc"),
    pjoin("util", "stringprintf.cc"),
    pjoin("util","strutil.cc"),
    pjoin("util","valgrind.cc"),
    pjoin("re2", "bitstate.cc"),
    pjoin("re2", "compile.cc"),
    pjoin("re2", "dfa.cc"),
    pjoin("re2", "filtered_re2.cc"),
    pjoin("re2", "mimics_pcre.cc"),
    pjoin("re2", "nfa.cc"),
    pjoin("re2", "onepass.cc"),
    pjoin("re2", "parse.cc"),
    pjoin("re2", "perl_groups.cc"),
    pjoin("re2", "prefilter.cc"),
    pjoin("re2", "prefilter_tree.cc"),
    pjoin("re2", "prog.cc"),
    pjoin("re2", "re2.cc"),
    pjoin("re2", "regexp.cc"),
    pjoin("re2", "set.cc"),
    pjoin("re2", "simplify.cc"),
    pjoin("re2", "tostring.cc"),
    pjoin("re2", "unicode_casefold.cc"),
    pjoin("re2", "unicode_groups.cc")
]

for i, f in enumerate(re2_cpp_src):
    re2_cpp_src[i] = pjoin(RE2_SRC_PATH, f)

INSTALL_H_FILES = [ "filtered_re2.h",
                    "re2.h",
                    "set.h",
                    "stringpiece.h",
                    "variadic_function.h"]

if os.path.exists(RE2_INSTALL_PATH):
    shutil.rmtree(RE2_INSTALL_PATH)
install_include_path = pjoin(RE2_INSTALL_PATH, "include", "re2")
makedirs(install_include_path)
for f in INSTALL_H_FILES:
    shutil.copyfile(pjoin(RE2_SRC_PATH, "re2", f), 
                    pjoin(install_include_path, f))

re2_ext = Extension( "re2._re2",
        sources=re2_cpp_src+['re2/_re2.pyx'],
        language="c++",
        include_dirs=['re2_cpp', pjoin('re2', 'src')],
        extra_compile_args=['-Wno-unused-function'],
    )

# re2_ext = Extension( "re2.tester",
#         sources=['re2/tester.pyx'],
#         language="c++",
#         include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
#         libraries=["re2"],
#         library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#         runtime_library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#         extra_compile_args=['-Wno-unused-function']
#     )

is_py_3 = int(sys.version_info[0] > 2)
cython_ext_list = cythonize(re2_ext, compile_time_env={'IS_PY_THREE': is_py_3})

setup(
    name="re2",
    maintainer=get_authors(),
    packages=['re2'],
    ext_modules=cython_ext_list,
    version="0.2.20",
    description=DESCRIPTION,
    long_description=get_long_description(),
    license=LICENSE,
    maintainer_email = EMAIL,
    url = "http://github.com/Wyss/pyre2/",
    classifiers = CLASSIFIERS,
)

