"""Broken Interfaces Handling"""

from ZODB.interfaces import IBroken
from ZODB.broken import Broken
from ZODB.broken import broken_cache
from ZODB.broken import find_global

from zope.interface.interface import InterfaceClass
from zope.interface import declarations

orig_ProvidesClass = declarations.ProvidesClass


class BrokenInterfaceClass(InterfaceClass):
    """An interface whose module is no longer available."""

    def __reduce__(self):
        """Use ZODB.broken's missing tolerant global handling."""
        return (find_global, (self.__module__, self.__name__))


class ProvidesClass(orig_ProvidesClass):
    
    def __init__(self, cls, *interfaces):
        return super(ProvidesClass, self).__init__(
            cls, *rebuildBrokenInterfaces(*interfaces))


def rebuildBrokenInterfaces(*interfaces):
    for iface in interfaces:
        cls = iface.__class__
        if (cls is type and
            len(iface.__bases__) == 1 and
            iface.__bases__[0] is Broken):
            broken_cache.pop((iface.__module__, iface.__name__,))
            yield find_global(
                iface.__module__, iface.__name__,
                Broken=IBroken, type=BrokenInterfaceClass)
        else:
            yield iface
