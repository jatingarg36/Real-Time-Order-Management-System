import psycopg2

conn = psycopg2.connect(
    dbname="test_db",
    user="workspace",
    password="",
    host="localhost",
    port="5432"
)

def create_orders_tables():
    with conn.cursor() as cursor:
        cursor.execute(open("db_setup.sql", "r").read())


create_orders_tables()
