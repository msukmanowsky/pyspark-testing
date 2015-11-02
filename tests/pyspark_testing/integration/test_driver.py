from ... import relative_file
from . import PySparkIntegrationTest

from pyspark_testing import driver
from pyspark_testing.models import BroadbandCoverageInfo


class TestDriver(PySparkIntegrationTest):

    def setUp(self):
        self.data = (self.sc.textFile(driver.data_path(), use_unicode=False)
                    .map(lambda l: l.decode('latin_1'))
                    .map(BroadbandCoverageInfo.from_csv_line))


    # def test_top_unserved(self):
        # driver.top_unserved()

    def test_summary_stats(self):
        expected_stats = {
            'broadband_available': 8714,
            'broadband_unavailable': 41285,
            'dsl_available': 14858,
            'dsl_unavailable': 35141,
            'wireless_available': 30971,
            'wireless_unavailable': 19028
        }
        self.assertDictEqual(expected_stats, driver.summary_stats(self.data))
