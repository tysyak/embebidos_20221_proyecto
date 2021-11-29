#!/usr/bin/env python3

import psycopg2 as psy
from os import getenv

class BD:
    def __init__(self):
        """!
        Esta clase solo se encarga de conectar la base de datos. implementada en
        Postgresql.
        """
        self.conn = psy.connect(
            user=getenv("PGUSER"),
            password=getenv("PGPASSWORD"),
            host=getenv("PGHOST"),
            port="5432",
            database=getenv("PGDATABASE")
        )

    def ejecutar_consulta(self, query, un_resultado=True):
        """!
        Ejecuta la consulta
        @param query Es la consulta que se realizará
        @param un_resultado Se esfecifica en True si solo se espera una fila de
        resultados, False si se espera varias filas, por defecto esta en True

        @return Ua o unas tuplas de resultados
        """
        cur = self.conn.cursor()
        cur.execute(query)
        if (un_resultado):
            return cur.fetchone()
        return cur.fetchall()
