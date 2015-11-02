import re
import sys

from setuptools import setup, find_packages

# Get version without importing, which avoids dependency issues
def get_version():
    with open('pyspark_testing/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')

def readme():
    with open('README.md') as f:
        return f.read()

install_requires = []
lint_requires = [
    'pep8',
    'pyflakes'
]

if sys.version_info.major < 3:
    tests_require = ['mock', 'nose', 'unittest2']
else:
    tests_require = ['mock', 'nose']

dependency_links = []
setup_requires = []
if 'nosetests' in sys.argv[1:]:
    setup_requires.append('nose')

setup(
    name='pyspark_testing',
    version=get_version(),
    author='Mike Sukmanowsky',
    author_email='mike.sukmanowsky@gmail.com',
    url='https://github.com/msukmanowsky/pyspark-testing',
    description=('Examples of unit and integration testing with PySpark'),
    long_description=readme(),
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require={
        'test': tests_require,
        'all': install_requires + tests_require,
        'docs': ['sphinx'] + tests_require,
        'lint': lint_requires
    },
    dependency_links=dependency_links,
    test_suite='nose.collector',
    include_package_data=True,
)
