"""Broken Interfaces Handling"""

from ZODB import interfaces
from ZODB.broken import Broken

from zope.interface import interface
from zope.interface import declarations

orig_normalizeargs = declarations._normalizeargs


def _normalizeargs(sequence, *args, **kw):
    """Handle broken objects assuming they should be interfaces."""
    cls = sequence.__class__
    if (cls is type and
        len(sequence.__bases__) == 1 and
        sequence.__bases__[0] is Broken):
        iface = interface.InterfaceClass(
            sequence.__name__, (interfaces.IBroken, ),
            __module__=sequence.__module__)
        return orig_normalizeargs(iface, *args, **kw)
    return orig_normalizeargs(sequence, *args, **kw)
