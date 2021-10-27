from setuptools import setup, find_packages  # Always prefer setuptools over distutils

__title__ = 'kiwiplot'
__version__ = '0.1.0'
__license__ = 'MIT'


with open('Readme.md') as f:
    readme = f.read()
with open('Changelog.md') as f:
    changelog = f.read()

setup(
    name=__title__,
    version=__version__,
    description='Fast beautiful plots using Qt',
    long_description=readme + '\n\n' + changelog,
    packages=find_packages(),
    url='tbd', # Homepage.
    author='Dr. John',
    author_email='tbd',
    license=__license__,
    python_requires='>=3.6',
)
