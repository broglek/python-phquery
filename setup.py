#!/usr/bin/python

from distutils.core import setup, Extension

setup (name = 'phquery',
       version = '0.4',
       description = 'A simple module for getting info from a PH/QI server.',
       author = "John N. Laliberte",
       author_email = 'allanonjl@gentoo.org',
       maintainer = "Matthew Miller",
       maintainer_email = 'mattdm@mattdm.org',
       url='http://www.mattdm.org/misc/python-ph/',
       classifiers=['Development Status :: 4 - Beta',
                    'Intended Audience :: Developers',
                    'Intended Audience :: System Administrators',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Communications :: Email :: Address Book',
                    'Topic :: Internet',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: System :: Networking',
                    'Topic :: System :: Systems Administration :: Authentication/Directory'
                    ],
       py_modules = ['phquery']
       )
