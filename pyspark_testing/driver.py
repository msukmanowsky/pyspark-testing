#!/usr/bin/env python
from operator import add
import warnings
import pkg_resources
import os
import pprint

try:
    from pyspark import SparkContext
except ImportError:
    warnings.warn('Cannot import pyspark.SparkContext, certain driver functions '
                  'will not work')


from pyspark_testing.models import BroadbandCoverageInfo


def data_path():
    resource_path = os.path.join('data', 'National_Broadband_Data_March2012_Eng.csv')
    return pkg_resources.resource_filename('pyspark_testing', resource_path)


def top_unserved(data, n=10):
    '''
    What are the top n largest areas that don't have broadband connections?
    '''
    return (data.filter(lambda d: d.unserved != 0)
            .sortBy(lambda d: d.population, ascending=False)
            .take(n))


def summary_stats(data):
    def stats_gen(d):
        for k in ('dsl', 'wireless', 'broadband'):
            if getattr(d, '{}_available'.format(k)):
                yield ('{}_available'.format(k), 1)
            else:
                yield ('{}_unavailable'.format(k), 1)

    return data.flatMap(stats_gen).foldByKey(0, add).collectAsMap()

def main():
    '''
    Driver entry point for spark-submit.
    '''
    with SparkContext() as sc:
        data = (sc.textFile(data_path(), use_unicode=False)
                .map(lambda l: l.decode('latin_1'))
                .map(BroadbandCoverageInfo.from_csv_line))

        pprint.pprint(data.first())
        # BroadbandCoverageInfo(hexagon_number=40930, gsa_number=None, first_nation=None, location_name=u'Aalders Landing, NS @ 44.82\xef\xbf\xbdN x 64.94\xef\xbf\xbdW', municipality=u'Annapolis, Subd. D :SC', latitude=44.82, longitude=-64.94, population=154, unserved=0, is_deferral_account=False, dsl_available=False, broadband_available=False, wireless_available=True)

        # What are the top 10 largest that don't have broadband connections?
        pprint.pprint(top_unserved(data))

        # What are the overall stats for availability by connection type?
        pprint.pprint(summary_stats(data))

if __name__ == '__main__':
    main()
