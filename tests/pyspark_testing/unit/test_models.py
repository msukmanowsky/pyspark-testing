import unittest

from pyspark_testing.models import BroadbandCoverageInfo


class TestModels(unittest.TestCase):

    def setUp(self):
        self.line = '40930,,,"Aalders Landing, NS @ 44.82\xb0N x 64.94\xb0W","Annapolis, Subd. D :SC",44.82,-64.94,154,"0","F","F","F","T"\r\n'
        self.line = self.line.decode('latin_1').strip()

    def test_broadband_coverage_info(self):
        info = BroadbandCoverageInfo.from_csv_line(self.line)
        expected_info = BroadbandCoverageInfo(hexagon_number=40930, gsa_number=None, first_nation=None, location_name=u'Aalders Landing, NS @ 44.82\xb0N x 64.94\xb0W', municipality=u'Annapolis, Subd. D :SC', latitude=44.82, longitude=-64.94, population=154, unserved=0, is_deferral_account=False, dsl_available=False, broadband_available=False, wireless_available=True)
        self.assertEqual(expected_info, info)
