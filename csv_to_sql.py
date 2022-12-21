# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 10:19:42 2022

@authors: Zack Goldblum, Josh Miller, Kevin Ramirez Chavez
"""

import os
import pandas as pd
import sqlite3

def csv_to_sql(csv_dir, sql_dir, name, cols):
    """
    This function creates SQL databases from the data within CSV files

    Arguments
    ---------
        csv_dir (str): directory of the CSV files
        sql_dir (str): directory for the SQL databases
        name (str): name of the SQL database to create
        cols (list): list of columns from the CSV file to add to the SQL database 
    
    Returns
    -------
        None
    """

    sql_filepath = os.path.join(sql_dir, name + ".sqlite")

    if not os.path.exists(sql_filepath):
        print(name + ".sqlite does not exist.\nCreating...\n-------------------")
        print("Reading CSV:\t", name + ".csv")
        csv_filepath = os.path.join(csv_dir, name + ".csv")
        df = pd.read_csv(csv_filepath)
        df_temp = df[cols]

        print("Creating table:\t", name)
        db = sqlite3.connect(sql_filepath)

        if name == "patients":
            db.execute("""CREATE TABLE IF NOT EXISTS patients(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject_id INTEGER,
            gender VARCHAR(1),
            anchor_age INTEGER)""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO patients (subject_id, gender, anchor_age)
                    VALUES (?,?,?)
                    ''',
                    (row.subject_id, 
                    row.gender,
                    row.anchor_age, )
                    )
            db.commit()

        elif name == "pharmacy":
            db.execute(f"""CREATE TABLE IF NOT EXISTS pharmacy(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject_id INTEGER,
            medication TEXT)""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO pharmacy (subject_id, medication)
                    VALUES (?, ?)
                    ''',
                    (row.subject_id, 
                    row.medication, ) 
                    )
            db.commit()

        elif name == "admissions":
            db.execute(f"""CREATE TABLE IF NOT EXISTS admissions(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject_id INTEGER,
            deathtime VARCHAR(30))""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO admissions (subject_id, deathtime)
                    VALUES (?, ?)
                    ''',
                    (row.subject_id, 
                    row.deathtime, ) 
                    )
            db.commit()

        elif name == "diagnoses_icd":
            db.execute(f"""CREATE TABLE IF NOT EXISTS diagnoses_icd(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject_id INTEGER,
            icd_code VARCHAR(60))""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO diagnoses_icd (subject_id, icd_code)
                    VALUES (?, ?)
                    ''',
                    (row.subject_id, 
                    row.icd_code, ) 
                    )
            db.commit()

        elif name == "icustays":
            db.execute(f"""CREATE TABLE IF NOT EXISTS icustays(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject_id INTEGER,
            first_careunit INTEGER)""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO icustays (subject_id, first_careunit)
                    VALUES (?, ?)
                    ''',
                    (row.subject_id, 
                    row.first_careunit, ) 
                    )
            db.commit()
        
        elif name == "d_icd_diagnoses":
            db.execute(f"""CREATE TABLE IF NOT EXISTS d_icd_diagnoses(
            row_idx INTEGER PRIMARY KEY AUTOINCREMENT, 
            icd_code VARCHAR(60),
            long_title TEXT )""")
            for row in df_temp.itertuples():
                db.execute('''
                    INSERT INTO d_icd_diagnoses (icd_code, long_title)
                    VALUES (?, ?)
                    ''',
                    (row.icd_code, 
                    row.long_title, ) 
                    )
            db.commit()

        print("Done:", sql_filepath, "\n")
        db.close()