# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 19:30:40 2022

@authors: Zack Goldblum, Josh Miller, Kevin Ramirez Chavez
"""

import pandas as pd
import sqlite3


def sql_to_df(sql_path, sql_query):
    """
    This function converts a SQL database into a Pandas DataFrame

    Arguments
    --------
        sql_path (str): path to the SQL database
        sql_query (str): SQL query

    Returns
    -------
        df (Pandas DataFrame): contains the queried SQL data
    """

    conn = sqlite3.connect(sql_path)
    cur = conn.cursor()
    cur.execute(sql_query)
    rows = cur.fetchall()
    if len(rows) == 0:
        print('No results returned for SQL query.')
    else:
        df = pd.DataFrame(rows)
        df.columns = [x[0] for x in cur.description]
        return df