from __future__ import print_function
from functools import partial
import atexit
import glob
import logging
import os
import sys
import subprocess
import time
import unittest

from pyspark_testing.version import __version__ as version

from ... import relative_file


log = logging.getLogger(__name__)
here = partial(relative_file, __file__)


def initialize_pyspark(spark_home, app_name, add_files=None):
    py4j = glob.glob(os.path.join(spark_home, 'python', 'lib', 'py4j*.zip'))[0]
    pyspark_path = os.path.join(spark_home, 'python')

    add_files = add_files or []
    sys.path.insert(0, py4j)
    sys.path.insert(0, pyspark_path)
    for file in add_files:
        sys.path.insert(0, file)

    from pyspark.context import SparkContext
    logging.getLogger('py4j.java_gateway').setLevel(logging.WARN)
    sc = SparkContext(appName=app_name, pyFiles=add_files)
    log.debug('SparkContext initialized')
    return sc


class PySparkIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not hasattr(cls, 'sc'):
            spark_home = os.environ['SPARK_HOME']
            build_zip = here('../../../dist/pyspark_testing-{}.tar.gz'.format(version))
            app_name = '{} Tests'.format(cls.__name__)
            cls.sc = initialize_pyspark(spark_home, app_name, [build_zip])
            log.debug('SparkContext initialized on %s', cls.__name__)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'sc'):
            cls.sc.stop()
