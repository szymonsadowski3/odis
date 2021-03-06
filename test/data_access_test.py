import datetime
import os
import unittest
from psycopg2.extras import RealDictRow

from src.rest_api.db.data_access import *
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
        self.cursor.execute("DROP TABLE IF EXISTS class_of_ips;")
        self.cursor.execute("""
                create table class_of_ips
                (
                    name varchar(255),
                    ips text[]
                );
        """)
        with open("test_data/ip_traffic_test_data.sql") as file_in:
            for line in file_in:
                self.cursor.execute(line)
        self.connection.commit()


    def tearDown(self):
        self.connection.close()

    def test_surround_with_quotes(self):
        self.assertEqual(surround_with_quotes("test"), "'test'")

    def test_list_to_pgarray(self):
        self.assertEqual(list_to_pgarray(['test1', 'test2']), '{{"test1","test2"}}')

    def test_is_array_empty(self):
        self.assertEqual(is_array_empty([]), True)
        self.assertEqual(is_array_empty(['a']), False)

    def test_is_parameter_empty(self):
        self.assertEqual(is_parameter_empty([]), True)
        self.assertEqual(is_parameter_empty(None), True)
        self.assertEqual(is_parameter_empty('a'), False)

    def helper_test_values_by_dictionary(self, record, test_values_dictionary):
        compared_attributes = [
            'port_src', 'port_dst',
            'ip_src', 'ip_dst'
        ]
        for compared_attribute in compared_attributes:
            self.assertEqual(record[compared_attribute], test_values_dictionary["{}_in".format(compared_attribute)][0])

    def helper_test_ip_traffic_records(self, all_data, test_values_dictionary=None):
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
                if test_values_dictionary:
                    self.helper_test_values_by_dictionary(record, test_values_dictionary)

    def test_get_all_data(self):
        all_data = get_all_data()
        self.assertEqual(len(all_data), 500)
        self.helper_test_ip_traffic_records(all_data)

    def test_get_all_data_paginated(self):
        all_data = get_all_data_paginated(1, 10)
        self.assertEqual(len(all_data), 10)
        self.helper_test_ip_traffic_records(all_data)

    def test_insert_class_of_ips(self):
        insert_class_of_ips("test", ["0.0.0.0"])
        classes = get_all_classes_of_ips()
        self.assertGreater(len(classes), 0)
        self.assertEqual(classes[0]['name'], 'test')

    def test_delete_class_of_ips(self):
        insert_class_of_ips("test", ["0.0.0.0"])
        len_before = len(get_all_classes_of_ips())
        delete_class_of_ips("test")
        len_after = len(get_all_classes_of_ips())
        self.assertEquals(len_before-1, len_after)

    def test_get_class_of_ips(self):
        insert_class_of_ips("test", ["0.0.0.0"])
        ipclass = get_class_of_ips("test")
        self.assertEqual(ipclass, [RealDictRow([('name', 'test'), ('ips', [['0.0.0.0']])])])

    def test_edit_class_of_ips(self):
        insert_class_of_ips("test", ["0.0.0.0"])
        edit_class_of_ips("test", ["1.1.1.1"])
        classes = get_all_classes_of_ips()
        self.assertListEqual(classes[0]['ips'], [["1.1.1.1"]])

    def test_get_all_classes_of_ips(self):
        insert_class_of_ips("test", ["0.0.0.0"])
        classes = get_all_classes_of_ips()
        self.assertGreater(len(classes), 0)
        self.assertEqual(classes[0]['name'], 'test')

    def test_get_filtered_data(self):
        filtering_request = {
            "bytes_between": [
                2000,
                None
            ],
            "incoming_outgoing_in": [
                "incoming"
            ],
            "ip_dst_in": [
                "10.0.2.15"
            ],
            "ip_proto_in": [
                "tcp"
            ],
            "ip_src_in": [
                "173.194.188.231"
            ],
            "limit": 10,
            "packets_between": [
                0,
                2
            ],
            "page": 0,
            "port_dst_in": [
                "42294"
            ],
            "port_src_in": [
                "443"
            ],
            "stamp_between": [
                "2020-03-27 21:02:01.000000",
                None
            ]
        }
        data = get_filtered_data(filtering_request)
        self.assertLessEqual(len(data), 10)
        self.helper_test_ip_traffic_records(data, filtering_request)

    def test_aggregation(self):
        data = get_aggregation(
            "bytes",
            "sum",
            "day",
            [
                "2020-03-27 21:02:01.000000",
                None
            ]
        )
        self.assertListEqual(
            data,
            [
                RealDictRow([('label', datetime.datetime(2020, 4, 20, 0, 0)), ('value', 4042832)]),
                RealDictRow([('label', datetime.datetime(2020, 4, 25, 0, 0)), ('value', 40)]),
            ]
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
