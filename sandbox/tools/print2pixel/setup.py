#!/usr/bin/env python

# Learned it all here: http://ianbicking.org/docs/setuptools-presentation/
# and here: http://peak.telecommunity.com/DevCenter/setuptools


try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Dynamically fetch the version, licence, and readme
version = __import__('print2pixel').__version__
license = __import__('print2pixel').__license__
#readme = file('README.txt','rb').read()

setup(name='print2pixel',
        version = version,
        scripts = ['print2pixel.py'],
        py_modules=['print2pixel'],
        description='Printing optimization utility for pixel to print, paper size, and unit conversions',
        #long_description=readme,
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        platforms='OS Independent',
        license=license,
        test_suite = 'tests.run_doc_tests',
        keywords='digital maps,print maps,dpi,ppi,resolution',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
        ],
        packages=find_packages(),
        zip_safe=False,
        )