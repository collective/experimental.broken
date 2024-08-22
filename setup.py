from setuptools import setup, find_packages
import os

tests_require = ['zope.testing']

setup(name='experimental.broken',
      version='0.6',
      description="Better ZODB handling of broken interfaces and components",
      long_description=(open("README.rst").read() + '\n\n' + 
                        open(os.path.join("docs", "HISTORY.rst")).read()),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='https://github.com/rpatterson/experimental.broken',
      license='ZPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
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
      extras_require=dict(test=tests_require,
                          registry=['zope.component'],
                          zcml=['collective.monkeypatcher']),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
