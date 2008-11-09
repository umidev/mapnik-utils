from distutils.core import setup

# Dynamically calculate the version.
version = __import__('nik2img').__version__

setup(name='nik2img',
        version = version,
        py_modules=['nik2img'],
        description='A mapfile to image converter for Mapnik',
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=['Development Status :: Beta',
                     'Environment :: Desktop or Web Environment',
                     'Framework :: Mapnik',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Utilities'],
        scripts = ['nik2img.py'],
        )