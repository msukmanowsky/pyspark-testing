#!/usr/bin/env bash
set -e
SPARK_VERSION='1.5.1'
HADOOP_VERSION='2.4'

wget http://www.apache.org/dyn/closer.lua/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz /tmp/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
tar -xzf /tmp/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
