import psycopg2


def create_databases() -> None:
    conn = psycopg2.connect(
        dbname="notes",
        user="postgres",
        password="182713",
        port="5432",
        host="localhost"
    )

    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id serial primary key,
            name_notes text NOT NULL,
            notes text NOT NULL
        ); 
        """)

    conn.commit()
    conn.close()


def save_notes(name:str, notes_text:str):
    conn = psycopg2.connect(
        dbname="notes",
        user="postgres",
        password="182713",
        port="5432",
        host="localhost"
    )

    with conn.cursor() as cursor:
        cursor.execute("insert into note (name_notes, notes) values ((%s), (%s));", (name, notes_text))

    conn.commit()
    conn.close()


def get_notes_from_db() -> list:
    conn = psycopg2.connect(
        dbname="notes",
        user="postgres",
        password="182713",
        port="5432",
        host="localhost"
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM public.note")

        result = cursor.fetchall()

        print(result)
        print(type(result))

    conn.commit()
    conn.close()

    return result


def delete_notes_from_db(name:str) -> list:
    conn = psycopg2.connect(
        dbname="notes",
        user="postgres",
        password="182713",
        port="5432",
        host="localhost"
    )

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM public.note WHERE name_notes = (%s);", (name, ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    get_notes_from_db()
