

from setuptools import setup, find_packages
import sys, os

version = '1.0'


setup(name='django-ui-widgets',
      version=version,
      description="Library of django ui widgets",
      long_description="""\
                        Library of django forms widgets and fields
                        """,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords=['django', 'forms', 'widgets', 'fields', 'django-ui'],
      author='Alexander',
      author_email='digital-mag@ya.ru',
      url='https://github.com/Sanshain/django-ui-widgets',
      license='AGPL',

      packages=['django-ui-widgets'],
      include_package_data=True,
      install_requires=["Django>=2.0"],

      entry_points="""
      # -*- Entry points: -*-
      """,
      )