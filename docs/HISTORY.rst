Changelog
=========

0.4 - Unreleased
----------------

- Fix ZODB.broken.Broken pickling so that non-persistent component
  registrations don't interfere with committing changes to a
  persistent registry.
  [rossp]

0.3 - 2011-11-07
----------------

- Pickle broken interfaces in such a way that they can be unpickled
  without this package being installed.
  [rossp]

- Fix component registrations such that they can be used to unregister
  broken registrations.
  [rossp]


0.2 - 2011-11-06
----------------

- Add configure.zcml and z3c.autoinclude support for applying the
  patches under Plone.
  [rossp]


0.1 - 2011-11-06
----------------

- Initial release.
  [rossp]
