=====
pyre2
=====

Summary
=======

pyre2 is a Python extension that wraps
`Google's RE2 regular expression library
<http://code.google.com/p/re2/>`_.

This version of pyre2 is similar to the one you'd
find at `facebook's github repository <http://github.com/facebook/pyre2/>`_
except that the stated goal of this version is to be a *drop-in replacement* for
the ``re`` module.


This version differs from `axiak <https://github.com/axiak/pyre2>`_ in the 
following way:

* Python 3 support (no test suite for Python 2 but looks promising)
* Uses the type of the pattern to determine the encoding of the output.
* Builds statically against google/re2 included as a subtree instead of a library::

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
never have. For example, ``RE2`` does not handle lookahead assertions
(``(?=...)``).
For this reason, the module will automatically fall back to the original 
``re`` module if there is a regex that it cannot handle.

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

Installation
============

To install in Python 3, you must first install the prerequisites:

* The Python development headers
* A build environment with ``clang++`` or ``g++``
* cython

Then run::
    
    $ python setup.py install

For Python 2 the -Wshorten-64-to-32 flag needs to not be used (shows up on OS X)
, so we need to overide the CFLAGS for Unicode to work.  First run::

    $ python setup.py build_ext --inplace


So if you see a bunch of warnings re-run with below::

    
    $ CFLAGS="-O3" python setup.py install

and it has been shown to work.

Unicode Support
===============

In Python 3 Unicode and Bytes strings using ASCII character set run almost as 
fast as each other (semi-experimentally proven) and for most loads at least 
twice as fast. For searching on UTF-8 Unicode using non-ascii, use the 
``re.UNICODE`` flag to get the results properly encoded and spans properly 
calculated.

Internally, all Unicode strings get encoded to UTF-8 and are manipulated as
bytestrings until a call for results is made.   

Mixing types will get you zero output but it will work, as it would using 
standard lib re module:

* bytes pattern arg + bytes string --> bytes output
* unicode pattern arg + unicode string --> unicode output
* unicode pattern arg + bytes string --> unicode output

Tests
=====

run tests in ``tests/``
More tests welcomes

Missing Features
================

Currently the features missing are:

* If you use substitution methods without a callback, a non 0/1 maxsplit 
argument is not supported.


Credits
=======

* https://github.com/axiak/pyre2
* https://github.com/facebook/pyre2
