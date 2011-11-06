import unittest
from zope.testing import doctest

from zope import interface
import persistent


class IFoo(interface.Interface): pass


class Foo(persistent.Persistent): pass


def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        optionflags=(
            doctest.ELLIPSIS|
            doctest.NORMALIZE_WHITESPACE|
            doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
