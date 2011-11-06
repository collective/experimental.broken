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
    >>> zope.interface.alsoProvides(foo_one, tests.IFoo)

    >>> foo_one.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_one))
    [<InterfaceClass experimental.broken.tests.IFoo>]

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

When the patches are applied, the object behaves properly.
`
    >>> from zope.interface import declarations
    >>> from experimental.broken import interface
    >>> declarations._normalizeargs = interface._normalizeargs

    >>> conn_three = db.open()
    >>> root_three = conn_three.root()
    >>> foo_three = root_three['foo']

    >>> foo_three.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_three))
    [<InterfaceClass experimental.broken.interface.IBroken>]

The interface can be removed.

    >>> zope.interface.noLongerProvides(foo_three, interface.IBroken)
    >>> transaction.commit()

    >>> conn_four = db.open()
    >>> root_four = conn_four.root()
    >>> foo_four = root_four['foo']

    >>> foo_four.bar
    'bar'
    >>> list(zope.interface.directlyProvidedBy(foo_four))
    []
