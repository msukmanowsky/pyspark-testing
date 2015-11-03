#!/usr/bin/env bash
#
# Assumes you're working inside an active virtualenv
python=`which python`
PYSPARK_PYTHON=$python PYSPARK_DRIVER_PYTHON=$python $SPARK_HOME/bin/spark-submit pyspark_testing/driver.py "$@"
