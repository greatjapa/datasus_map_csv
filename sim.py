import csv
import sys
import hashlib
import json

with open('municipios.json') as f:
    MUNICIPIOS = json.load(f)

with open('cid.json') as f:
    CID = json.load(f)

FIELDNAMES = [
    "NUMERODO",
    "CODINST",
    "TIPOBITO",
    "DTOBITO",
    "HORAOBITO",
    "NATURAL",
    "DTNASC",
    "IDADE",
    "SEXO",
    "RACACOR",
    "ESTCIV",
    "ESC",
    "OCUP",
    "CODMUNRES",
    "LOCOCOR",
    "CODESTAB",
    "CODMUNOCOR",
    "IDADEMAE",
    "ESCMAE",
    "OCUPMAE",
    "QTDFILVIVO",
    "QTDFILMORT",
    "GRAVIDEZ",
    "GESTACAO",
    "PARTO",
    "OBITOPARTO",
    "PESO",
    "NUMERODN",
    "OBITOGRAV",
    "OBITOPUERP",
    "ASSISTMED",
    "EXAME",
    "CIRURGIA",
    "NECROPSIA",
    "LINHAA",
    "LINHAB",
    "LINHAC",
    "LINHAD",
    "LINHAII",
    "CAUSABAS",
    "CB_PRE",
    "DTATESTADO",
    "CIRCOBITO",
    "ACIDTRAB",
    "FONTE",
    "TPPOS",
    "DTINVESTIG",
    "CAUSABAS_O",
    "DTCADASTRO",
    "ATESTANTE",
    "FONTEINV",
    "DTRECEBIM"
]

def calc_idade(value):        
    if value[0] == "1":
        return str(int(value[1:])) + " horas"
    if value[0] == "2":
        return str(int(value[1:])) + " dias"
    if value[0] == "3":
        return str(int(value[1:])) + " meses"
    if value[0] == "4":
        return str(int(value[1:])) + " anos"
    if value[0] == "5":
        return str(int(value[1:])) + " anos"
    return "Idade ignorada"

TIPOBITO = {
    "1": "obito fetal",
    "2": "obito nao fetal",
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

ESTCIV = {
    "1": "Solteiro",
    "2": "Casado",
    "3": "Viuvo",
    "4": "Separado judicialmente/Divorciado",
    "9": "Ignorado",
}

ESC = {
    "1": "Nenhuma",
    "2": "1 a 3 anos",
    "3": "4 a 7 anos",
    "4": "8 a 11 anos",
    "5": "12 e mais",
    "9": "Ignorado"
}

LOCOCOR = {
    "1": "Hospital",
    "2": "Outro estab saude",
    "3": "Domicilio",
    "4": "Via Publica",
    "5": "Outros",
    "9": "Ignorado"
}

ESCMAE = {
    "1": "Nenhuma",
    "2": "1 a 3 anos",
    "3": "4 a 7 anos",
    "4": "8 a 11 anos",
    "5": "12 e mais",
    "9": "Ignorado"
}

GRAVIDEZ = {
    "1": "Unica",
    "2": "Dupla",
    "3": "Tripla e mais",
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

PARTO = {
    "1": "Vaginal",
    "2": "Cesareo",
    "9": "Ignorado"
}

OBITOPARTO = {
    "1": "Antes",
    "2": "Durante",
    "3": "Depois",
    "9": "Ignorado"
}

OBITOGRAV = {
    "1": "Sim",
    "2": "Nao",
    "9": "Ignorado"
}

OBITOPUERP = {
    "1": "Sim: ate 42 dias",
    "2": "SIm: de 43 dias a 01 ano",
    "3": "Nao",
    "9": "Ignorado"
}

ASSISTMED = {
    "1": "Com assistencia",
    "2": "Sem assistencia",
    "9": "Ignorado"
}

EXAME = {
    "1": "Sim",
    "2": "Nao",
    "9": "Ignorado"
}

CIRURGIA = {
    "1": "Sim",
    "2": "Nao",
    "9": "Ignorado"
}

NECROPSIA = {
    "1": "Sim",
    "2": "Nao",
    "9": "Ignorado"
}

CIRCOBITO = {
    "1": "Acidente",
    "2": "Suicidio",
    "3": "Homicidio",
    "4": "Outros",
    "9": "Ignorado"
}

ACIDTRAB = {
    "1": "Sim",
    "2": "Nao",
    "9": "Ignorado"
}

FONTE = {
    "1": "Boletim de Ocorrencia",
    "2": "Hospital",
    "3": "Familia",
    "4": "Outra",
    "9": "Ignorado"
}

TPPOS = {
    "1": "Sim",
    "2": "Nao"
}

ATESTANTE = {
    "1": "Sim",
    "2": "Substituto",
    "3": "IML",
    "4": "SVO",
    "5": "Outros"
}

FONTEINV = {
    "1": "Comite de Morte Materna e/ou Infantil",
    "2": "Visita domiciliar / Entrevista familia",
    "3": "Estab Saude / Prontuario",
    "4": "Relacion com outros bancos de dados",
    "5": "SVO",
    "6": "IML",
    "7": "Outra fonte",
    "8": "Multiplas fontes",
    "9": "Ignorado"
}

def enrich(row):
    row["IDADE"] = calc_idade(row["IDADE"])

    row["TIPOBITO"] = TIPOBITO.get(row['TIPOBITO'], row['TIPOBITO'])
    row["SEXO"] = SEXO.get(row['SEXO'], row['SEXO'])
    row["RACACOR"] = RACACOR.get(row['RACACOR'], row['RACACOR'])
    row["ESTCIV"] = ESTCIV.get(row['ESTCIV'], row['ESTCIV'])
    row["ESC"] = ESC.get(row['ESC'], row['ESC'])
    row["CODMUNRES"] = MUNICIPIOS.get(row["CODMUNRES"], row["CODMUNRES"])
    row["LOCOCOR"] = LOCOCOR.get(row['LOCOCOR'], row['LOCOCOR'])
    row["GRAVIDEZ"] = GRAVIDEZ.get(row['GRAVIDEZ'], row['GRAVIDEZ'])
    row["ESCMAE"] = ESCMAE.get(row['ESCMAE'], row['ESCMAE'])
    row["GESTACAO"] = GESTACAO.get(row['GESTACAO'], row['GESTACAO'])
    row["PARTO"] = PARTO.get(row['PARTO'], row['PARTO'])
    row["CODMUNOCOR"] = MUNICIPIOS.get(row["CODMUNOCOR"], row["CODMUNOCOR"])
    row["CAUSABAS"] = CID.get(row["CAUSABAS"], row["CAUSABAS"])
    row["CAUSABAS_O"] = CID.get(row["CAUSABAS_O"], row["CAUSABAS_O"])
    row["OBITOPARTO"] = OBITOPARTO.get(row['OBITOPARTO'], row['OBITOPARTO'])
    row["OBITOGRAV"] = OBITOGRAV.get(row['OBITOGRAV'], row['OBITOGRAV'])
    row["OBITOPUERP"] = OBITOPUERP.get(row['OBITOPUERP'], row['OBITOPUERP'])
    row["ASSISTMED"] = ASSISTMED.get(row['ASSISTMED'], row['ASSISTMED'])
    row["EXAME"] = EXAME.get(row['EXAME'], row['EXAME'])
    row["CIRURGIA"] = CIRURGIA.get(row['CIRURGIA'], row['CIRURGIA'])
    row["NECROPSIA"] = NECROPSIA.get(row['NECROPSIA'], row['NECROPSIA'])
    row["CIRCOBITO"] = CIRCOBITO.get(row['CIRCOBITO'], row['CIRCOBITO'])
    row["ACIDTRAB"] = ACIDTRAB.get(row['ACIDTRAB'], row['ACIDTRAB'])
    row["FONTE"] = FONTE.get(row['FONTE'], row['FONTE'])
    row["TPPOS"] = TPPOS.get(row['TPPOS'], row['TPPOS'])
    row["ATESTANTE"] = ATESTANTE.get(row['ATESTANTE'], row['ATESTANTE'])
    row["FONTEINV"] = FONTEINV.get(row['FONTEINV'], row['FONTEINV'])
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