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
version = __import__('nik2img').__version__
license = __import__('nik2img').__license__
readme = file('README.txt','rb').read()

setup(name='nik2img',
        version = version,
        py_modules=['nik2img'],
        description='A mapfile to image converter for the Mapnik C++/Python mapping toolkit',
        long_description=readme,
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        platforms='OS Independent',
        license=license,
        requires=['Mapnik'],
        test_suite = 'tests.run_doc_tests',
        keywords='Mapnik,gis,geospatial',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities'
        ],
        scripts = ['nik2img.py'],
        #packages=['niktests'],
        packages=find_packages(exclude=['tests','data','niktests']),
        zip_safe=False,
        #package_dir={'niktests': 'niktests'},
        package_data={'niktest': ['data/*']},
        )