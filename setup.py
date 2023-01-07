'''
References:
https://docs.python.org/3/distutils/setupscript.html#distutils-installing-package-data
https://stackoverflow.com/questions/24347450/how-do-you-add-additional-files-to-a-wheel
https://stackoverflow.com/questions/61624018/include-extra-file-in-a-python-package-using-setuptools
'''
from setuptools import setup, find_packages  # Always prefer setuptools over distutils

__title__ = 'kiwiplot'
__version__ = '0.1.1'
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
    include_package_data=True,
    package_data={__title__: ['images/*.png', '../kiwiplot_examples/*.py']},
    #data_files=[('examples', ['../kiwplot_examples/b1.gif', 'bm/b2.gif']), #another option for including examples
    # url='tbd', # Homepage.
    author='Dr. John',
    # author_email='tbd',
    license=__license__,
    python_requires='>=3.6',
)
