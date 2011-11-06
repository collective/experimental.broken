"""Broken Interfaces Handling"""

from ZODB.broken import Broken
from zope import interface
from zope.interface import declarations

orig_normalizeargs = declarations._normalizeargs


class IBroken(interface.Interface):
    """An interface whose module is no longer available."""


def _normalizeargs(sequence, *args, **kw):
    """Handle broken objects assuming they should be interfaces."""
    cls = sequence.__class__
    if (cls is type and
        len(sequence.__bases__) == 1 and
        sequence.__bases__[0] is Broken):
        return orig_normalizeargs(IBroken, *args, **kw)
    return orig_normalizeargs(sequence, *args, **kw)
