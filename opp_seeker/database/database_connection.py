from opp_seeker.general_params import DB_DSN

import psycopg2
from psycopg2 import pool
from threading import Lock

class Database_connection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._pool = psycopg2.pool.SimpleConnectionPool(1, 10, DB_DSN)

        return cls._instance

    def get_connection(self):
        return self._pool.getconn()

    def release_connection(self, conn):
        self._pool.putconn(conn)