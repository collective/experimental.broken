.. -*-doctest-*-

==========================
Broken Interfaces Handling
==========================

Start with a ZODB root with a basic object in it which provides an
interface.

    >>> from ZODB.DemoStorage import DemoStorage
    >>> from ZODB.DB import DB
    >>> storage = DemoStorage()
    >>> db = DB(storage)

    >>> from experimental.broken import tests
    >>> db.open().root()['foo'] = foo_one = tests.Foo()
    >>> foo_one.bar = 'bar'

    >>> import zope.interface
    >>> IFoo = tests.IFoo
    >>> zope.interface.alsoProvides(foo_one, IFoo)

    >>> from ZODB import interfaces
    >>> foo_one.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_one))
    [<InterfaceClass experimental.broken.tests.IFoo>]
    >>> IFoo.providedBy(foo_one)
    True
    >>> interfaces.IBroken.providedBy(foo_one)
    False

    >>> import transaction
    >>> transaction.commit()

When the code that an interface originally came from has been removed,
zope.interface operations on objects in the ZODB which directly
provide that interface will fail.

    >>> del tests.IFoo
    >>> tests.reset()

    >>> foo_two = db.open().root()['foo']
    >>> foo_two.bar
    Traceback (most recent call last):
    TypeError: ("'type' object is not iterable", <function Provides at 0x...>, (<class 'experimental.broken.tests.Foo'>, <class 'experimental.broken.tests.IFoo'>))
    >>> list(zope.interface.directlyProvidedBy(foo_two))
    Traceback (most recent call last):
    TypeError: ("'type' object is not iterable", <function Provides at 0x...>, (<class 'experimental.broken.tests.Foo'>, <class 'experimental.broken.tests.IFoo'>))
    >>> IFoo.providedBy(foo_two)
    Traceback (most recent call last):
    TypeError: ("'type' object is not iterable", <function Provides at 0x...>, (<class 'experimental.broken.tests.Foo'>, <class 'experimental.broken.tests.IFoo'>))
    >>> interfaces.IBroken.providedBy(foo_two)
    Traceback (most recent call last):
    TypeError: ("'type' object is not iterable", <function Provides at 0x...>, (<class 'experimental.broken.tests.Foo'>, <class 'experimental.broken.tests.IFoo'>))

When the patches are applied, the object behaves properly.

    >>> from experimental.broken import interface
    >>> from zope.interface import declarations
    >>> declarations.ProvidesClass = interface.ProvidesClass
    >>> tests.reset()

    >>> foo_three = db.open().root()['foo']
    >>> foo_three.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_three))
    [<BrokenInterfaceClass experimental.broken.tests.IFoo>]
    >>> IFoo.providedBy(foo_three)
    True
    >>> interfaces.IBroken.providedBy(foo_three)
    True

The object can be committed back to the database when the code is
missing and the patches are applied.

    >>> foo_three._p_changed = True
    >>> transaction.commit()

If the code is restored after the object has previously been committed
to the ZODB without the code, the object behaves as it did before the
code was removed in the first place.

    >>> declarations.ProvidesClass = interface.orig_ProvidesClass
    >>> tests.IFoo = IFoo
    >>> tests.reset()
    >>> foo_four = db.open().root()['foo']

    >>> foo_four.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_four))
    [<InterfaceClass experimental.broken.tests.IFoo>]
    >>> IFoo.providedBy(foo_four)
    True
    >>> interfaces.IBroken.providedBy(foo_four)
    False

The interface can be removed even when the code is not available.

    >>> del tests.IFoo
    >>> declarations.ProvidesClass = interface.ProvidesClass
    >>> tests.reset()

    >>> foo_five = db.open().root()['foo']
    >>> zope.interface.noLongerProvides(foo_five, interfaces.IBroken)
    >>> transaction.commit()

    >>> foo_six = db.open().root()['foo']
    >>> foo_six.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_six))
    []
    >>> IFoo.providedBy(foo_six)
    False
    >>> interfaces.IBroken.providedBy(foo_six)
    False
