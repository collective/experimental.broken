from setuptools import setup, find_packages
import os

tests_require = ['zope.testing']

setup(name='experimental.broken',
      version='0.1',
      description="Better ZODB handling of broken interfaces and components",
      long_description=
      open(os.path.join(
          "experimental", "broken", "README.txt")).read() + '\n\n' +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/rpatterson.listfile',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['experimental'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ZODB3',
          'zope.interface',
      ],
      test_suite = "experimental.broken.tests.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
