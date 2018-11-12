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

def to_hash(*args):
    hash = hashlib.md5()
    for arg in args:
        hash.update(arg.encode())
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
            ID_INTEGRACAO text,
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
        if len(row["DTNASC"]) > 0 and row["SEXO"] != "Ignorado" and len(row["RACACOR"]) > 0 and (row["LOCOCOR"] == "Hospital" or row["LOCOCOR"] == "Outro estab saude"):
            DTNASC = get_date_1(row['DTNASC'])
            SEXO = row["SEXO"]
            RACACOR = row["RACACOR"]
            CODMUNRES = row['CODMUNRES']
            DTOBITO = get_date_1(row['DTOBITO'])
            LOCOCOR = row['LOCOCOR']
            CAUSABAS = row['CAUSABAS']

            ID_INTEGRACAO = to_hash(DTNASC.isoformat(), SEXO, RACACOR, CODMUNRES, DTOBITO.isoformat(), "Com obito")
            c.execute('''INSERT INTO sim (ID_INTEGRACAO, SEXO, RACACOR, DTNASC, CODMUNRES, DTOBITO, LOCOCOR, CAUSABAS) VALUES (?,?,?,?,?,?,?,?)''', (ID_INTEGRACAO,SEXO,RACACOR,DTNASC,CODMUNRES,DTOBITO,LOCOCOR,CAUSABAS))

    sihsus_sql = """
        CREATE TABLE sihsus (
            ID integer PRIMARY KEY, 
            ID_INTEGRACAO text,
            ID_ATENDIMENTO text,
            SEXO text,
            RACA_COR text,
            NASC date,
            MUNIC_RES text,
            CEP text,
            DT_INTER date,
            DT_SAIDA date,
            DIAG_PRINC text,
            MORTE text
    );"""

    c.execute(sihsus_sql)

    for i in range(0, 12):
        attend = get_attend(i)
        for row in attend:
            if row["RACA_COR"] != "Ignorado":
                NASC = get_date_1(row['NASC'])
                SEXO = row["SEXO"]
                RACA_COR = row["RACA_COR"]
                MUNIC_RES = row['MUNIC_RES']
                CEP = row['CEP']
                DT_INTER = get_date_2(row['DT_INTER'])
                DT_SAIDA = get_date_2(row['DT_SAIDA'])
                DIAG_PRINC = row['DIAG_PRINC']
                MORTE = row["MORTE"]

                ID_INTEGRACAO = to_hash(NASC.isoformat(), SEXO, RACA_COR, MUNIC_RES, DT_SAIDA.isoformat(), MORTE)
                ID_ATENDIMENTO = to_hash(NASC.isoformat(), SEXO, RACA_COR, MUNIC_RES, CEP)
                c.execute('''INSERT INTO sihsus (ID_INTEGRACAO, ID_ATENDIMENTO, SEXO, RACA_COR, NASC, MUNIC_RES, CEP, DT_INTER, DT_SAIDA, DIAG_PRINC, MORTE) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (ID_INTEGRACAO,ID_ATENDIMENTO,SEXO,RACA_COR,NASC,MUNIC_RES,CEP,DT_INTER,DT_SAIDA,DIAG_PRINC,MORTE))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()