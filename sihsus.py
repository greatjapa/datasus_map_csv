import csv
import sys
import os

FIELDNAMES = [
    "UF_ZI",
    "ANO_CMPT",
    "MES_CMPT",
    "ESPEC",
    "CGC_HOSP",
    "N_AIH",
    "IDENT",
    "CEP",
    "MUNIC_RES",
    "NASC",
    "SEXO",
    "UTI_MES_TO",
    "MARCA_UTI",
    "UTI_INT_TO",
    "DIAR_ACOM",
    "QT_DIARIAS",
    "PROC_SOLIC",
    "PROC_REA",
    "VAL_SH",
    "VAL_SP",
    "VAL_TOT",
    "VAL_UTI",
    "US_TOT",
    "DT_INTER",
    "DT_SAIDA",
    "DIAG_PRINC",
    "DIAG_SECUN",
    "COBRANCA",
    "NATUREZA",
    "NAT_JUR",
    "GESTAO",
    "IND_VDRL",
    "MUNIC_MOV",
    "COD_IDADE",
    "IDADE",
    "DIAS_PERM",
    "MORTE",
    "NACIONAL",
    "CAR_INT",
    "HOMONIMO",
    "NUM_FILHOS",
    "INSTRU",
    "CID_NOTIF",
    "CONTRACEP1",
    "CONTRACEP2",
    "GESTRISCO",
    "INSC_PN",
    "SEQ_AIH5",
    "CBOR",
    "CNAER",
    "VINCPREV",
    "GESTOR_COD",
    "GESTOR_TP",
    "GESTOR_CPF",
    "GESTOR_DT",
    "CNES",
    "CNPJ_MANT",
    "INFEHOSP",
    "CID_ASSO",
    "CID_MORTE",
    "COMPLEX",
    "FINANC",
    "FAEC_TP",
    "REGCT",
    "RACA_COR",
    "ETNIA",
    "SEQUENCIA",
    "REMESSA",
    "AUD_JUST",
    "SIS_JUST",
    "VAL_SH_FED",
    "VAL_SP_FED",
    "VAL_SH_GES",
    "VAL_SP_GES",
    "VAL_UCI",
    "MARCA_UCI",
    "DIAGSEC1",
    "DIAGSEC2",
    "DIAGSEC3",
    "DIAGSEC4",
    "DIAGSEC5",
    "DIAGSEC6",
    "DIAGSEC7",
    "DIAGSEC8",
    "DIAGSEC9",
    "TPDISEC1",
    "TPDISEC2",
    "TPDISEC3",
    "TPDISEC4",
    "TPDISEC5",
    "TPDISEC6",
    "TPDISEC7",
    "TPDISEC8",
    "TPDISEC9"
]

SEXO = {
    "1": "1",
    "2": "2",
    "3": "3"
}

def enrich(row):
    row["SEXO"] = SEXO.get(row['SEXO'], row['SEXO'])
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