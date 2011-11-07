import unittest
from zope.testing import doctest

from zope import interface
from zope.interface import declarations
import persistent
from ZODB import broken


class IFoo(interface.Interface): pass


class Foo(persistent.Persistent): pass


def reset():
    declarations.InstanceDeclarations.clear()
    broken.broken_cache.clear()


def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        optionflags=(
            doctest.ELLIPSIS|
            doctest.NORMALIZE_WHITESPACE|
            doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
