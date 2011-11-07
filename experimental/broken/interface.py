"""Broken Interfaces Handling"""

from ZODB.interfaces import IBroken
from ZODB.broken import Broken
from ZODB.broken import broken_cache
from ZODB.broken import find_global

from zope.interface.interface import InterfaceClass
from zope.interface import declarations

orig_init = declarations.ProvidesClass.__init__
orig_reduce = InterfaceClass.__reduce__


def interface_reduce(self):
    """Use ZODB.broken's missing tolerant global handling."""
    # TODO this should be moved to zope.interface by implementing a
    # find_interface(modulename, globalname) function that in turn
    # calls:
    #   ZODB.broken.find_global(modulename, globalname,
    #                           Broken=IBroken, type=InterfaceClass)
    # then InterfaceClass.__reduce__ can just return:
    #   (find_interface, (self.__module__, self.__name__))
    # since there's no reason to pickle IBroken and InterfaceClass
    # with every interface.  We do for now however so that interface
    # pickles written while this patch was in effect will still work
    # if this patch is subsequently removed.
    if self is IBroken:
        return orig_reduce(self)
    return (find_global, (
        self.__module__, self.__name__, IBroken, InterfaceClass))


def __init__(self, cls, *interfaces):
    return orig_init(
        self, cls,
        *(rebuildBrokenInterface(iface) for iface in interfaces))


def rebuildBrokenInterface(iface):
    cls = iface.__class__
    if (cls is type and
        len(iface.__bases__) == 1 and
        iface.__bases__[0] is Broken):
        broken_cache.pop((iface.__module__, iface.__name__,))
        return find_global(
            iface.__module__, iface.__name__,
            Broken=IBroken, type=InterfaceClass)
    return iface
