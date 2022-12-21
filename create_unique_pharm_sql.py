# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 17:34:21 2022

@authors: Zack Goldblum, Josh Miller, Kevin Ramirez Chavez
"""

import os
import sys
import sqlite3
from bmes import tempdir

def create_unique_pharm_sql():
    """
    Create a SQL databse with only unique pharmacy rows 

    Arguments
    ---------
        None

    Returns
    -------
        None
    """

    sql_filepath_in = os.path.join(tempdir(), "final_project_sql", "pharmacy.sqlite")
    db = sqlite3.connect(sql_filepath_in)
    cur = db.cursor()
    cur.execute('''SELECT DISTINCT medication FROM pharmacy''')
    rows = cur.fetchall()
    db.close()

    sql_filepath_pharm = os.path.join(tempdir(), "final_project_sql", "pharmacy_unique.sqlite")
    if not os.path.exists(sql_filepath_pharm):
        print(f"Creating {sql_filepath_pharm}")
        db = sqlite3.connect(sql_filepath_pharm)
        
        db.execute("""CREATE TABLE   IF NOT EXISTS   pharmacy_unique ( 
            medication_unique TEXT)
            """)
        
        for row in rows:
            db.execute(''' INSERT INTO pharmacy_unique (medication_unique) 
                    VALUES (?) ''', 
                    (row[0], )
                    )
        
        db.commit()
        db.close()