import unittest
from zope.testing import doctest

from zope import interface
from zope.interface import declarations
import persistent
from ZODB import broken


class IFoo(interface.Interface): pass


class IBar(interface.Interface): pass


class IQux(interface.Interface): pass


class Bar(object):

    def __call__(self, *args, **kw): pass


class Foo(Bar, persistent.Persistent): pass


def reset():
    declarations.InstanceDeclarations.clear()
    broken.broken_cache.clear()


def tearDown(self=None, orig_ProvidesClass=declarations.ProvidesClass,
             orig_IFoo=IFoo, orig_IQux=IQux, orig_Foo=Foo, orig_Bar=Bar):
    reset()
    declarations.ProvidesClass = orig_ProvidesClass
    global IFoo
    IFoo = orig_IFoo
    global IQux
    IQux = orig_IQux
    global Foo
    Foo = orig_Foo
    global Bar
    Bar = orig_Bar


def test_suite():
    return doctest.DocFileSuite(
        'interface.txt',
        'registry.txt',
        tearDown=tearDown,
        optionflags=(
            doctest.ELLIPSIS|
            doctest.NORMALIZE_WHITESPACE|
            doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
