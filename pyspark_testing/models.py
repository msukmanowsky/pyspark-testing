import csv
import cStringIO as StringIO
import itertools


def safe_convert(string):
    if string == '':
        return None

    if string == 'T':
        return True
    elif string == 'F':
        return False

    try:
        return int(string)
    except ValueError:
        pass

    try:
        return float(string)
    except ValueError:
        pass

    return string


def unicode_csv_reader(unicode_csv_data, **kwargs):
    def encoder():
        for line in unicode_csv_data:
            try:
                yield line.encode('latin_1')
            except UnicodeEncodeError:
                raise Exception('Could not encode {!r} using "latin_1"'.format(line))

    reader = csv.reader(encoder(), **kwargs)
    for row in reader:
        yield [cell.decode('latin_1') for cell in row]


class BroadbandCoverageInfo(object):
    __slots__ = (
        # "Hexagon Number","GSA Number","First Nation","Location Name","Municipality","Latitude","Longitude","Total Population 2006 Census","Unserved / Underserved Population in Hexagon","Deferral Account","DSL Available","Cable Available","Wireless Available"
        'hexagon_number',        # Hexagon identifier (49,999 in total)
        'gsa_number',            # Geographic Service Area
        'first_nation',          # Name of first nations reserve
        'location_name',         # Name of location of hexagon
        'municipality',          # Municipality of hexagon
        'latitude',              # Latitudinal coordinate in decimal degrees
        'longitude',             # Longitudinal coordinate in decimal degrees
        'population',            # Total population in hexagon, from 2006 Census data
        'unserved',              # Estimated range of unserved / underserved population in hexagon (without 1.5 Mbps broadband service availability)
        'is_deferral_account',   # Location included in CRTC Decisions on Deferral Accounts
        'dsl_available',         # Indicates availability of DSL (Digital Subscriber Loop)
        'broadband_available',   # Indicates availability of Cable broadband service
        'wireless_available',    # Indicates availability of wireless broadband service
    )

    def __repr__(self):
        params = (p for p in self.__slots__ if not p.startswith('_'))
        params = ('{}={!r}'.format(p, getattr(self, p)) for p in params)
        params = ', '.join(params)
        return '{}({})'.format(self.__class__.__name__, params)

    __str__ = __repr__
    __unicode__ = unicode(__str__)

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        for k in self.__slots__:
            if getattr(self, k) != getattr(other, k):
                return False

        return True

    def __ne__(self, other):
        return not self.__equals__(other)

    @classmethod
    def from_csv_line(cls, line):
        # This is definitely not the most efficient way of reading CSV, but the
        # file contains some tricky quote chars
        reader = unicode_csv_reader((line,))
        parts = reader.next()
        parts = [safe_convert(p) for p in parts]
        kwargs = dict(zip(cls.__slots__, parts))

        return cls(**kwargs)
