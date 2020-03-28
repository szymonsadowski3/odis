from peewee import PostgresqlDatabase

pgdb = PostgresqlDatabase('postgres', user='odis', password='odis', host='localhost', port=5432)