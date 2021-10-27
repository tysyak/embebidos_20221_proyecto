#!/usr/bin/env python3

import psycopg2 as psy
from os import getenv

class BD:
    def __init__(self):
        self.conn = psy.connect(
            user=getenv("PGUSER"),
            password=getenv("PGPASSWORD"),
            host=getenv("PGHOST"),
            port="5432",
            database=getenv("PGDATABASE")
        )

    def ejecutar_consulta(self, query, un_resultado=True):
        cur = self.conn.cursor()
        cur.execute(query)
        if (un_resultado):
            return cur.fetchone()
        return cur.fetchall()
