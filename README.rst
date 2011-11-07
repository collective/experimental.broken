========================================
Experimental ZODB Broken Object Handling
========================================

WARNING!  This package is highly experimental and should not be used
by anyone but experts in the inner workings of the ZCA and the ZODB
and it should never be used in production.

The handling of broken objects by the ZODB can make an application
with add-ons that use zope.interface far too fragile.  If marker
interfaces from an add-on are used on objects in the ZODB, removing
that add-on can make any zope.interface operation on that object fail.
Even worse, if an add-on registers any components in a registry in the
ZODB, that entire registry will become unusable for any ZCA
operations.

Since the interfaces and the ZCA are often core parts of an
application using the ZODB, it may be appropriate to add special
handling for broken objects to those services.The patches included in
this package attempt to do just that.

For objects in the ZODB which directly provide a marker interface,
these patches allow that object to behave as without the application
of the marker interface if the interface is no longer available.  If
the interface is made available again, the full behavior of that
interface is restored.  Similarly, if a component whose class,
provided interface, or required interfaces are missing, these patches
allow the registry to perform lookups it would have been able to do
without the broken component registration.  If the component
class, provided interface, and required interfaces are restored,
then the component registration is fully restored.  If an object or
registry in the ZODB is committed to the ZODB with broken interfaces
or components, the commit will succeed and it is still possible to
fully restore previous behavior if the missing classes and interfaces
are restored.

The one exception is when the class of a *non-persistent* component
registered in a persistent registry is removed, the registry cannot be
successfully committed back to the ZODB.  IOW, if your persistent
registry contains a registration for a component whose base classes do
*not* include persistent.Persistent, then you'll be able to *use* the
registry but you won't be able to make any changes to the registry
without first removing the broken component registration.

The intention of this package is to see if the implementation of
broken object handling is correct and robust enough to merge into
zope.interface and zope.component themselves.  IOW, when this code is
found to be robust enough to use more widely, this package won't be
the home for it.  So once again, unless you are a senior Zope
developer, do not use these patches.

If you want to try this package out, work only on a copy of your ZODB,
never on the live data, and simply add this package to your instance's
eggs.  It uses z3c.autoinclude to automatically apply the patches
under a Plone instance.
