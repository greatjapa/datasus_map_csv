import csv
import sys

FIELDNAMES = [
    "NUMERODN",
    "CODINST",
    "CODESTAB",
    "CODMUNNASC",
    "LOCNASC",
    "IDADEMAE",
    "ESTCIVMAE",
    "ESCMAE",
    "CODOCUPMAE",
    "QTDFILVIVO",
    "QTDFILMORT",
    "CODMUNRES",
    "GESTACAO",
    "GRAVIDEZ",
    "PARTO",
    "CONSULTAS",
    "DTNASC",
    "HORANASC",
    "SEXO",
    "APGAR1",
    "APGAR5",
    "RACACOR",
    "PESO",
    "IDANOMAL",
    "CODANOMAL",
    "DTRECEBIM"
]

LOCNASC = {
    "9": "Ignorado",
    "1": "Hospital",
    "2": "Outro Estab Saude",
    "3": "Domicilio",
    "4": "Outros"
}

ESTCIVMAE = {
    "1": "Solteira",
    "2": "Casada",
    "3": "Viuva",
    "4": "Separado judicialmente/Divorciado",
    "9": "Ignorado",
}

ESCMAE = {
    "1": "Nenhuma",
    "2": "1 a 3 anos",
    "3": "4 a 7 anos",
    "4": "8 a 11 anos",
    "5": "12 e mais",
    "9": "Ignorado"
}

GESTACAO = {
    "1": "Menos de 22 semanas",
    "2": "22 a 27 semanas",
    "3": "28 a 31 semanas",
    "4": "32 a 36 semanas",
    "5": "37 a 41 semanas",
    "6": "42 semanas e mais",
    "9": "Ignorado"
}

GRAVIDEZ = {
    "1": "Unica",
    "2": "Dupla",
    "3": "Tripla e mais",
    "9": "Ignorado"
}

PARTO = {
    "1": "Vaginal",
    "2": "Cesareo",
    "9": "Ignorado"
}

CONSULTAS = {
    "1": "Nenhuma",
    "2": "de 1 a 3",
    "3": "de 4 a 6",
    "4": "7 e mais",
    "9": "Ignorado"
}

SEXO = {
    "0": "Ignorado",
    "1": "Masculino",
    "2": "Feminino"
}

RACACOR = {
    "1": "Branca",
    "2": "Preta",
    "3": "Amarela",
    "4": "Parda",
    "5": "Indigena"
}

IDANOMAL = {
    "9": "Ignorado",
    "1": "Sim",
    "2": "Nao"
}

def enrich(row):
    row["LOCNASC"] = LOCNASC.get(row['LOCNASC'], row['LOCNASC'])
    row["ESTCIVMAE"] = ESTCIVMAE.get(row['ESTCIVMAE'], row['ESTCIVMAE'])
    row["ESCMAE"] = ESCMAE.get(row['ESCMAE'], row['ESCMAE'])
    row["GESTACAO"] = GESTACAO.get(row['GESTACAO'], row['GESTACAO'])
    row["GRAVIDEZ"] = GRAVIDEZ.get(row['GRAVIDEZ'], row['GRAVIDEZ'])
    row["PARTO"] = PARTO.get(row['PARTO'], row['PARTO'])
    row["CONSULTAS"] = CONSULTAS.get(row['CONSULTAS'], row['CONSULTAS'])
    row["SEXO"] = SEXO.get(row['SEXO'], row['SEXO'])
    row["RACACOR"] = RACACOR.get(row['RACACOR'], row['RACACOR'])
    row["IDANOMAL"] = IDANOMAL.get(row['IDANOMAL'], row['IDANOMAL'])
    return row

def map(filename):
    with open(filename) as csv_in, open('e_' + filename, 'w') as csv_out:
        reader = csv.DictReader(csv_in)
        writer = csv.DictWriter(csv_out, fieldnames=FIELDNAMES, extrasaction='ignore')
        writer.writeheader()
        for row in reader:
            writer.writerow(enrich(row))

def main():
    map(sys.argv[1])

if __name__ == "__main__":
    main()