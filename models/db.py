import psycopg2


class Postgres:
    def __init__(self, *, db_name: str, db_host: str, db_port: str, db_user: str, db_password: str):
        self.database = db_name
        self.user = db_user

        self.conn = psycopg2.connect(
            database=db_name,
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
