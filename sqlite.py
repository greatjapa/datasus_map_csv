import csv
import sys
import json
import sqlite3
import hashlib
from datetime import date, datetime

def read(filename):
    result = []
    with open(filename) as csv_in:
        reader = csv.DictReader(csv_in)
        for row in reader:
            result.append(row)
    return result

def get_sinasc():
    sinasc = read("e_DNPR2016.csv")
    print("nascimento:", len(sinasc))
    return sinasc

def get_sim():
    sim = read("e_DOPR2016.csv")
    print("mortalidade:", len(sim))
    return sim

def get_attend(i):
    attend_filenames = [
        "e_RDPR1601.csv",
        "e_RDPR1602.csv",
        "e_RDPR1603.csv",
        "e_RDPR1604.csv",
        "e_RDPR1605.csv",
        "e_RDPR1606.csv",
        "e_RDPR1607.csv",
        "e_RDPR1608.csv",
        "e_RDPR1609.csv",
        "e_RDPR1610.csv",
        "e_RDPR1611.csv",
        "e_RDPR1612.csv"
    ]
    filename = attend_filenames[i]
    atted = read(filename)
    print("total attendimento mes", i + 1, len(atted))
    return atted

def generate_sim_id(row):
    hash = hashlib.md5()
    hash.update(row["DTNASC"].encode())
    hash.update(row["SEXO"].encode())
    hash.update(row["RACACOR"].encode())
    hash.update(row["CODMUNRES"].encode())
    return hash.hexdigest() 

def generate_sihsus_id(row):
    hash = hashlib.md5()
    hash.update(row["NASC"].encode())
    hash.update(row["SEXO"].encode())
    hash.update(row["RACA_COR"].encode())
    hash.update(row["MUNIC_RES"].encode())
    return hash.hexdigest() 

def get_date_1(value):
    if len(value) == 8:
        day = int(value[0:2])
        month = int(value[2:4])
        year = int(value[4:8])
        return date(year, month, day)
    return None

def get_date_2(nasc):
    if len(nasc) == 8:
        year = int(nasc[0:4])
        month = int(nasc[4:6])
        day = int(nasc[6:8])
        return date(year, month, day)
    return None

def main():
    sim_sql = """
        CREATE TABLE sim (
            ID integer PRIMARY KEY, 
            IDENTIDADE text,
            SEXO text,
            RACACOR text,
            DTNASC date,
            CODMUNRES text,
            DTOBITO date,
            LOCOCOR text,
            CAUSABAS text
    );"""

    conn = sqlite3.connect("sim_sihsus.sqlite")
    c = conn.cursor()
    c.execute(sim_sql)

    for row in get_sim():
        if len(row["DTNASC"]) > 0 and (row["LOCOCOR"] == "Hospital" or row["LOCOCOR"] == "Outro estab saude"):
            IDENTIDADE = generate_sim_id(row)
            SEXO = row["SEXO"]
            RACACOR = row["RACACOR"]
            DTNASC = get_date_1(row['DTNASC'])
            CODMUNRES = row['CODMUNRES']
            DTOBITO = get_date_1(row['DTOBITO'])
            LOCOCOR = row['LOCOCOR']
            CAUSABAS = row['CAUSABAS']
            c.execute('''INSERT INTO sim (IDENTIDADE, SEXO, RACACOR, DTNASC, CODMUNRES, DTOBITO, LOCOCOR, CAUSABAS) VALUES (?,?,?,?,?,?,?,?)''', (IDENTIDADE,SEXO,RACACOR,DTNASC,CODMUNRES,DTOBITO,LOCOCOR,CAUSABAS))

    sihsus_sql = """
        CREATE TABLE sihsus (
            ID integer PRIMARY KEY, 
            IDENTIDADE text,
            SEXO text,
            RACA_COR text,
            NASC date,
            MUNIC_RES text,
            DT_INTER date,
            DT_SAIDA date,
            DIAG_PRINC text
    );"""

    c.execute(sihsus_sql)

    for i in range(0, 12):
        attend = get_attend(i)
        for row in attend:
            if row['MORTE'] == 'Com obito':
                IDENTIDADE = generate_sihsus_id(row)
                SEXO = row["SEXO"]
                RACA_COR = row["RACA_COR"]
                NASC = get_date_1(row['NASC'])
                MUNIC_RES = row['MUNIC_RES']
                DT_INTER = get_date_2(row['DT_INTER'])
                DT_SAIDA = get_date_2(row['DT_SAIDA'])
                DIAG_PRINC = row['DIAG_PRINC']
                c.execute('''INSERT INTO sihsus (IDENTIDADE, SEXO, RACA_COR, NASC, MUNIC_RES, DT_INTER, DT_SAIDA, DIAG_PRINC) VALUES (?,?,?,?,?,?,?,?)''', (IDENTIDADE,SEXO,RACA_COR,NASC,MUNIC_RES,DT_INTER,DT_SAIDA,DIAG_PRINC))


    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()