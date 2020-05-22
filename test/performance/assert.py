import os
import unittest

from src.rest_api.db.db_configuration import get_connection
from test.performance.config import HOW_MANY_RECORDS_FOR_TEST


class DataAccessCase(unittest.TestCase):
    def test_after_performance_test_execution(self):
        os.environ['IS_TEST'] = 'True'
        print("setting up database stuff...")
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT COUNT(1) FROM ip_traffic")
        result = self.cursor.fetchall()
        self.assertEqual(result[0][0], HOW_MANY_RECORDS_FOR_TEST)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
