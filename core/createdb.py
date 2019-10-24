"""
Alessandro Makzanini
CODE NOT CALLED FROM DJANGO, JUST USED IN Dockerfile for create user and db after app start
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
from psycopg2.extensions import AsIs


if __name__ == "__main__":

    try:
        con = psycopg2.connect(dbname='postgres',
                               user='postgres',
                               password='postgres')

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

        cur = con.cursor()

        cur.execute("create user %s with password %s", (AsIs('cath_user'), '11235813post',))


        # Use the psycopg2.sql module instead of string concatenation
        # in order to avoid sql injection attacs.
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('cath_local'))
        )
        print("Database creation proces done...can run Cathedral Studio image now")
    except Exception:
        print("Exception in DB creation proces....passing")