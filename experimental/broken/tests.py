import unittest
from zope.testing import doctest

from zope import interface
from zope.interface.interface import InterfaceClass
from zope.interface import declarations
from zope.component import persistentregistry
import persistent
from ZODB import broken
import transaction


class IFoo(interface.Interface): pass


class IBar(interface.Interface): pass


class IQux(interface.Interface): pass


class Bar(object):

    def __call__(self, *args, **kw): pass


class Foo(Bar, persistent.Persistent): pass


def reset():
    declarations.InstanceDeclarations.clear()
    broken.broken_cache.clear()


def tearDown(self=None,
             orig_reduce=InterfaceClass.__reduce__,
             orig_provides_init=declarations.ProvidesClass.__init__,
             orig_registry_setstate=
             persistentregistry.PersistentAdapterRegistry.__setstate__,
             orig_IFoo=IFoo, orig_IQux=IQux, orig_Foo=Foo, orig_Bar=Bar):
    reset()
    transaction.abort()
    InterfaceClass.__reduce__ = orig_reduce
    declarations.ProvidesClass.__init__ = orig_provides_init
    persistentregistry.PersistentAdapterRegistry.__setstate__ = (
        orig_registry_setstate)
    if '__setstate__' in persistentregistry.PersistentComponents.__dict__:
        del persistentregistry.PersistentComponents.__setstate__
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
        'broken.txt',
        tearDown=tearDown,
        optionflags=(
            doctest.ELLIPSIS|
            doctest.NORMALIZE_WHITESPACE|
            doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
