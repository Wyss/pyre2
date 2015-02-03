=====
pyre2
=====

.. contents::

Summary
=======

pyre2 is a Python extension that wraps
`Google's RE2 regular expression library
<http://code.google.com/p/re2/>`_.

This version of pyre2 is similar to the one you'd
find at `facebook's github repository <http://github.com/facebook/pyre2/>`_
except that the stated goal of this version is to be a *drop-in replacement* for
the ``re`` module.


grinner This version differs from `axiak <https://github.com/axiak/pyre2>` in the following way:

* Python 3 support
* Uses the type of the pattern to determine the encoding of the output.
Mixing types will get you zero output but it will work, as it would using 
standard lib re module:

    bytes pattern arg + bytes string --> bytes output
    unicode pattern arg + unicode string --> unicode output
    unicode pattern arg + bytes string --> unicode output

* Builds against google/re2 included as a submodule.  I couldn't get a linked
library build to work on system Python in OS X (only self build Python) so 
I went with the easiest and most portable solution for a C++

    git subtree add --prefix re2/src/re2 git@github.com:google/re2.git master --squash

* Updated cython C++ code for newer cython features.

Backwards Compatibility
=======================

The stated goal of this module is to be a drop-in replacement for ``re``. 
My hope is that some will be able to go to the top of their module and put::

    try:
        import re2 as re
    except ImportError:
        import re

That being said, there are features of the ``re`` module that this module may
never have. For example, ``RE2`` does not handle lookahead assertions (``(?=...)``).
For this reason, the module will automatically fall back to the original ``re`` module
if there is a regex that it cannot handle.

However, there are times when you may want to be notified of a failover. For this reason,
I'm adding the single function ``set_fallback_notification`` to the module.
Thus, you can write::

    try:
        import re2 as re
    except ImportError:
        import re
    else:
	re.set_fallback_notification(re.FALLBACK_WARNING)

And in the above example, ``set_fallback_notification`` can handle 3 values:
``re.FALLBACK_QUIETLY`` (default), ``re.FALLBACK_WARNING`` (raises a warning), and
``re.FALLBACK_EXCEPTION`` (which raises an exception).

**Note**: The re2 module treats byte strings as UTF-8. This is fully backwards compatible with 7-bit ascii.
However, bytes containing values larger than 0x7f are going to be treated very differently in re2 than in re.
The RE library quietly ignores invalid utf8 in input strings, and throws an exception on invalid utf8 in patterns.
For example:

    >>> re.findall(r'.', '\x80\x81\x82')
    ['\x80', '\x81', '\x82']
    >>> re2.findall(r'.', '\x80\x81\x82')
    []

If you require the use of regular expressions over an arbitrary stream of bytes, then this library might not be for you.

Installation
============

To install, you must first install the prerequisites:

* The Python development headers (e.g. *sudo apt-get install python-dev*)
* A build environment with ``clang++`` or ``g++`` (e.g. *sudo apt-get install build-essential*)
* cython


    $ python setup.py install


If you want to make changes to the bindings, you must have Cython >=0.13.

Unicode Support
===============

One current issue is Unicode support. As you may know, ``RE2`` supports UTF8,
which is certainly distinct from unicode. Right now the module will automatically
encode any unicode string into utf8 for you, which is *slow* (it also has to
decode utf8 strings back into unicode objects on every substitution or split).
Therefore, you are better off using bytestrings in utf8 while working with RE2
and encoding things after everything you need done is finished.

Performance
===========


Current Status
==============

pyre2 has only received basic testing. Please use it
and let me know if you run into any issues!


Tests
=====

If you would like to help, one thing that would be very useful
is writing comprehensive tests for this. It's actually really easy:

* Come up with regular expression problems using the regular python 're' module.
* Write a session in python traceback format `Example <http://github.com/axiak/pyre2/blob/master/tests/search.txt>`_.
* Replace your ``import re`` with ``import re2 as re``.
* Save it as a .txt file in the tests directory. You can comment on it however you like and indent the code with 4 spaces.

Missing Features
================

Currently the features missing are:

* If you use substitution methods without a callback, a non 0/1 maxsplit argument is not supported.


Credits
=======

Though I ripped out the code, I'd like to thank David Reiss
and Facebook for the initial inspiration. Plus, I got to
gut this readme file!

Moreover, this library would of course not be possible if not for
the immense work of the team at RE2 and the few people who work
on Cython.
