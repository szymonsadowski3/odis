import datetime
import os
import unittest
from psycopg2.extras import RealDictRow

from src.rest_api.db.data_access import get_all_data
from src.rest_api.db.db_configuration import get_connection


class DataAccessCase(unittest.TestCase):
    def setUp(self):
        os.environ['IS_TEST'] = 'True'
        print("setting up database stuff...")
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE SCHEMA IF NOT EXISTS test")
        self.cursor.execute("SET search_path TO test")
        self.cursor.execute("DROP TABLE IF EXISTS ip_traffic;")
        self.cursor.execute("""
                create table ip_traffic
                (
                    event_type varchar(255),
                    ip_src varchar(255),
                    ip_dst varchar(255),
                    port_src varchar(255),
                    port_dst varchar(255),
                    timestamp_start timestamp,
                    timestamp_end timestamp,
                    packets integer,
                    bytes integer,
                    writer_id varchar(255),
                    mac_src varchar(255),
                    mac_dst varchar(255),
                    ip_proto varchar(255),
                    src_hostname varchar(255),
                    dst_hostname varchar(255),
                    incoming_outgoing varchar(255)
                );
        """)
        with open("test_data/ip_traffic_test_data.sql") as file_in:
            for line in file_in:
                self.cursor.execute(line)
        self.connection.commit()


    def tearDown(self):
        self.connection.close()


    def test_get_all_data(self):
        all_data = get_all_data()
        self.assertEqual(len(all_data), 500)
        for record in all_data:
            record_attributes = [
                'event_type',
                'ip_src',
                'ip_dst',
                'port_src',
                'port_dst',
                'timestamp_start',
                'timestamp_end',
                'packets',
                'bytes',
                'writer_id',
                'mac_src',
                'mac_dst',
                'ip_proto',
                'src_hostname',
                'dst_hostname',
                'incoming_outgoing',
            ]
            for record_attribute in record_attributes:
                self.assertTrue(record_attribute in record)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
