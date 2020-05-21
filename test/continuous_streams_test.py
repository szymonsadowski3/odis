import datetime
import unittest
from psycopg2.extras import RealDictRow

from src.rest_api.process.continuous_streams import find_continuous_streams
from test.test_data.data import database_ip_traffic_records, streams_to_find


class ContinuousStreamsCase(unittest.TestCase):
    def test_continuous_streams_finding(self):


        actual = find_continuous_streams(database_ip_traffic_records)

        self.assertListEqual(actual, streams_to_find)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
