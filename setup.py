from setuptools import setup, find_packages
import sys, os

version = '0.2.0'

setup(name='libclient',
      version=version,
      description="Python Client Library for Lightbase",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Danilo Carvalho',
      author_email='danilo.carvalho@lightbase.com.br',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'six',
          'requests==2.3.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
