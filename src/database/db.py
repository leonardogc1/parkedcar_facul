import psycopg2

#configurações do BD
host = 'localhost'
dbname = 'parked-car'
user = 'postgres'
password = 'ads2023'

conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

def get_connection():
    return psycopg2.connect(conn_string)