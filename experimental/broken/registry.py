"""Broken Interfaces Handling"""

from ZODB.interfaces import IBroken
from ZODB.broken import Broken
from ZODB.broken import broken_cache
from ZODB.broken import find_global

from zope.component import persistentregistry

from experimental.broken import interface

orig_setstate = persistentregistry.PersistentAdapterRegistry.__setstate__


def __setstate__(self, state):
    provided = state['_provided']
    for iface, order in provided.iteritems():
        cls = iface.__class__
        if (cls is type and
            len(iface.__bases__) == 1 and
            iface.__bases__[0] is Broken):
            broken_cache.pop((iface.__module__, iface.__name__,))
            broken_iface = find_global(
                iface.__module__, iface.__name__,
                Broken=IBroken, type=interface.BrokenInterfaceClass)
            del provided[iface]
            provided[broken_iface] = order
    return orig_setstate(self, state)
