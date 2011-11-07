========================================
Experimental ZODB Broken Object Handling
========================================

WARNING!  This package is highly experimental and should not be used
by anyone but experts in the inner workings of the ZCA and the ZODB
and it should never be used in production.

The handling of broken objects by the ZODB can leave make an
application that with add-ons that use zope.interface far too fragile.
If marker interfaces from an add-on are used on objects in the ZODB,
removing that add-on can make any zope.interface operation on that
object fail.  Even worse, if an add-on registers any components in a
registry in the ZODB, that entire registry will become unusable for
any ZCA operations.

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
component, provided interface, and required interfaces are restored,
then the component registration is fully restored.  If an object or
registry in the ZODB is committed to the ZODB with broken interfaces
or components, the commit will succeed and it is still possible to
fully restore previous behavior if the missing classes and interfaces
are restored.

The intention of this package is to see if the implementation of
broken object handling is correct and robust enough to merge into
zope.interface and zope.component themselves.  IOW, when this code is
found to be robust enough to use more widely, this package won't be
the home for it.  So once again, unless you are a senior Zope
developer, do not use these patches.
