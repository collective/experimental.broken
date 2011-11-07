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
    >>> conn_one = db.open()
    >>> root_one = conn_one.root()

    >>> from experimental.broken import tests
    >>> root_one['foo'] = foo_one = tests.Foo()
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

    >>> conn_two = db.open()
    >>> root_two = conn_two.root()
    >>> foo_two = root_two['foo']

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

    >>> from zope.interface import declarations
    >>> from experimental.broken import interface
    >>> declarations._normalizeargs = interface._normalizeargs

    >>> conn_three = db.open()
    >>> root_three = conn_three.root()
    >>> foo_three = root_three['foo']

    >>> foo_three.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_three))
    [<InterfaceClass experimental.broken.tests.IFoo>]
    >>> IFoo.providedBy(foo_three)
    True
    >>> interfaces.IBroken.providedBy(foo_three)
    True

The interface can be removed.

    >>> zope.interface.noLongerProvides(foo_three, interfaces.IBroken)
    >>> transaction.commit()

    >>> conn_four = db.open()
    >>> root_four = conn_four.root()
    >>> foo_four = root_four['foo']

    >>> foo_four.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_four))
    []
    >>> IFoo.providedBy(foo_four)
    False
    >>> interfaces.IBroken.providedBy(foo_four)
    False
