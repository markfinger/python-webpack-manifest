from setuptools import setup
from webpack_manifest import webpack_manifest

setup(
    name='webpack-manifest',
    version=webpack_manifest.__version__,
    packages=['webpack_manifest', 'webpack_manifest.templatetags'],
    description='Manifest loader that allows you to include references to files built by webpack',
    long_description='Documentation at https://github.com/markfinger/python-webpack-manifest',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/python-webpack-manifest',
)
