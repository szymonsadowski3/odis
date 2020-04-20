import datetime
import unittest
from psycopg2.extras import RealDictRow

from src.rest_api.process.continuous_streams import find_continuous_streams


class LearningCase(unittest.TestCase):
    def test_continuous_streams_finding(self):
        input_rows = [
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 9, 33)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 9, 48)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 20, 10)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 24, 24)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 27, 37)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 31, 49)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 40, 57)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 21, 56, 21)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
            RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', ''), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 22, 59, 54)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)])
        ]

        actual = find_continuous_streams(input_rows)
        expected = [
            {
                'stream_start': datetime.datetime(2020, 4, 19, 20, 9, 33),
                'stream_end': datetime.datetime(2020, 4, 19, 20, 9, 48),
                'total_time_in_seconds': 15,
                'records_in_stream': [
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 9, 33)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 9, 48)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)])
                ]
            },
            {
                'stream_start': datetime.datetime(2020, 4, 19, 20, 24, 24),
                'stream_end': datetime.datetime(2020, 4, 19, 20, 31, 49),
                'total_time_in_seconds': 445,
                'records_in_stream': [
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 24, 24)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 27, 37)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)]),
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 20, 31, 49)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)])
                ]
            },
            {
                'stream_start': datetime.datetime(2020, 4, 19, 21, 56, 21),
                'stream_end': datetime.datetime(2020, 4, 19, 21, 56, 21),
                'total_time_in_seconds': 0,
                'records_in_stream': [
                    RealDictRow([('event_type', None), ('ip_src', None), ('ip_dst', 'TEST'), ('port_src', None), ('port_dst', None), ('timestamp_start', datetime.datetime(2020, 4, 19, 21, 56, 21)), ('timestamp_end', None), ('packets', None), ('bytes', None), ('writer_id', None), ('mac_src', None), ('mac_dst', None), ('ip_proto', None), ('src_hostname', None), ('dst_hostname', None), ('incoming_outgoing', None)])
                ]
            }
        ]

        self.assertListEqual(actual, expected)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
