import psycopg2

conn = psycopg2.connect(
    dbname="test_db",
    user="workspace",
    password="",
    host="localhost",
    port="5432"
)

def create_required_tables():
    with conn.cursor() as cursor:
        print( cursor.execute(open("db_setup.sql", "r").read()))


create_required_tables()
