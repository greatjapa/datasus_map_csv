import csv
import sys

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

def map_with_sim():
    sim = get_sim()
    hash = {}
    for row in sim:
        hash[row['IDENTIFICACAO'] + row['CODMUNRES']] = True
    for i in range(0, 12):
        attend = get_attend(i)
        count = 0
        for row in attend:
            if hash.get(row['IDENTIFICACAO'] + row['MUNIC_RES'], False):
                count = count + 1
        print("em comum com tabela de mortalidade:", count)

def main():
    map_with_sim()

if __name__ == "__main__":
    main()