import psycopg2
def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id serial PRIMARY KEY,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
    id serial PRIMARY KEY,
    client_id integer REFERENCES clients (id),
    phone BIGINT
    );
    """)


def drop_db(cur):
    cur.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)

def new_client(cur, first_name, last_name, email):
    cur.execute("""
    INSERT INTO clients (first_name, last_name, email)
	VALUES ('%s', '%s', '%s') RETURNING *;
    """%(first_name, last_name, email))
    print(cur.fetchall())


def add_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phones (client_id, phone)
    VALUES (%s, %s) RETURNING *;
    """%(client_id, phone))
    print(cur.fetchall())


def change_data(cur, client_id, first_name=None, last_name=None, email=None):
    if first_name != None:
        cur.execute("""
        UPDATE clients SET first_name = '%s' WHERE id = %s 
        RETURNING *;
        """%(first_name, client_id))
    if last_name != None:
        cur.execute("""
        UPDATE clients SET last_name = '%s' WHERE id = %s 
        RETURNING *;
        """%(last_name, client_id))
    if email != None:
        cur.execute("""
        UPDATE clients SET email = '%s' WHERE id = %s 
        RETURNING *;
        """%(email, client_id))
    print(cur.fetchall())


def del_phone(cur, client_id, phone):
    cur.execute("""
    DELETE FROM phones
	WHERE id = %s AND phone = %s;
    """%(client_id, phone))

    cur.execute("""
    SELECT * FROM phones
    """)
    print(cur.fetchall())


def del_client(cur, client_id):
    cur.execute("""
    DELETE FROM phones
    WHERE client_id = %s
    """%(client_id))

    cur.execute("""
    DELETE FROM clients
	WHERE id = %s;
    """%(client_id))

def find_client(cur, first_name=None, last_name=None, email=None):
    if first_name != None:
        cur.execute("""
        SELECT * FROM clients
       	WHERE first_name = '%s';
        """%(first_name))
    if last_name != None:
        cur.execute("""
        SELECT * FROM clients
        WHERE last_name = '%s';
        """%(last_name))
    if email != None:
        cur.execute("""
        SELECT * FROM clients
    	WHERE email = '%s';
        """%(email))
    print(cur.fetchall())

def find_client_using_phone(cur, phone):
    cur.execute("""
    SELECT * FROM phones p
    LEFT JOIN clients c ON p.client_id = c.id
    WHERE phone = %s
    """%(phone))
    print(cur.fetchall())


if __name__ == "__main__":
    with psycopg2.connect(database='clients_db', user='postgres', password='doka7744') as conn:
        with conn.cursor() as cur:
            drop_db(cur)
            create_db(cur)
            new_client(cur, 'vasya', 'pupkin', 'pupkin@mail.ru')
            new_client(cur, 'vasya', 'golenkov', 'gol@mail.ru')
            add_phone(cur, 1, 89232323233)
            add_phone(cur, 2, 89333333333)
            change_data(cur, 1, 'Vasyliy', 'pupkevich', 'pupkins@bk.ru')
            change_data(cur, 1, 'Vitaliy')
            del_phone(cur, 1, 89232323233)
            del_client(cur, 1)
            find_client(cur, 'vasya')
            find_client_using_phone(cur, 89333333333)
    conn.close()
