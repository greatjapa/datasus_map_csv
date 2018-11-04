import csv
import sys
import os
import hashlib

FIELDNAMES = [
    "IDENTIFICACAO",
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
    "1": "Masculino",
    "2": "Feminino",
    "3": "Feminino",
    "0": "Ignorado",
    "9": "Ignorado"
}

IDENT = {
    "1": "Normal",
    "5": "Longa permanencia",
    "0": "Outras/ignorado",
    "9": "Outras/ignorado"
}

GESTAO = {
    "1": "Estadual",
    "2": "Estadual plena",
    "3": "Municipal plena assist",
    "4": "Nao definida"
}

MORTE = {
    "1": "Com obito",
    "0": "Sem obito"
}

INSTRU = {
    "1": "Analfabeto",
    "2": "1 grau",
    "3": "2 grau",
    "4": "3 grau",
    "9": "Ignorado",
    "0": "Ignorado"
}

RACA_COR = {
    "01": "Branca",
    "02": "Preta",
    "03": "Parda",
    "04": "Amarela",
    "05": "Indigena",
    "99": "Ignorado"
}

REGCT = {
    "7100": "TABELA DE NAO GERACAO DE CREDITO POR PRODUCAO NA INTERNACAO E/OU AMBULATORIO",
    "7101": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO NA MEDIA COMPLEXIDADE AMBULATORIAL",
    "7102": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO NA MEDIA COMPLEXIDADE HOSPITALAR",
    "7103": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO NA ALTA COMPLEXIDADE AMBULATORIAL",
    "7104": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO NA ALTA COMPLEXIDADE HOSPITALAR",
    "7105": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO PARA OS PROCEDIMENTOS FINANCIADOS COM O FAEC",
    "7106": "ESTABELECIMENTO SEM GERACAO DE CREDITO TOTAL - EXCLUINDO FAEC",
    "7107": "ESTABELECIMENTO SEM GERACAO DE CREDITO NAS ACOES ESPEC. DE ODONTOLOGIA(INCENTIVO CEO I,II E III)",
    "7108": "ESTABELECIMENTO SEM GERACAO DE CREDITO(INCENTIVO A SAUDE DO TRABALHADOR)",
    "7109": "ESTABELECIMENTO SEM GERACAO DE CREDITO TOTAL-MEC",
    "7110": "ESTABELECIMENTO DE SAUDE DA ESTRUTURA DO MINISTERIO DA SAUDE - SEM GERACAO DE CREDITO TOTAL",
    "7111": "ESTABELECIMENTO DE SAUDE SEM GERACAO DE CREDITO - NASF, EXCETO FAEC",
    "7112": "ESTABELECIMENTO SEM GERACAO DE CREDITO TOTAL - INCLUINDO FAEC  - EXCLUSIVO PARA REDE SARAH",
    "7113": "ESTABELECIMENTO SEM GERACAO DE CREDITO TOTAL - INCLUINDO FAEC - OUTROS ESTABELECIMENTOS FEDERAIS",
    "7114": "ESTABELECIMENTO DE SAuDE SEM GERACAO DE CREDITO TOTAL, INCLUSIVE FAEC - PRONTO ATENDIMENTO",
    "7115": "ESTABELECIMENTO DE SAuDE SEM GERACAO DE CREDITO NA MEDIA COMPLEXIDADE - HU/MEC",
    "7116": "ESTABELECIMENTO DE SAuDE SEM GERACAO DE CREDITO NA MEDIA COMPLEXIDADE - LRPD",
    "7117": "Estabelecimento de Saude sem geracao de credito na media complexidade (exceto OPM) - CER",
    "0000": "Sem regra contratual"
}

FAEC_TP = {
    "010000": "Atencao Basica (PAB)",
    "020000": "Assistencia Farmaceutica",
    "040001": "Coleta de material",
    "040002": "Diagnostico em laboratorio clinico",
    "040003": "Coleta/exame anatomo-patologico colo uterino",
    "040004": "Diagnostico em neurologia",
    "040005": "Diagnostico em otorrinolaringologia/fonoaudiologia",
    "040006": "Diagnostico em psicologia/psiquiatria",
    "040007": "Consultas medicas/outros profissionais de nivel superior",
    "040008": "Atencao domiciliar",
    "040009": "Atendimento/acompanhamento em reabilitacao fisica, mental, visual, auditiva e multiplas defic",
    "040010": "Atendimento/acompanhamento psicossocial",
    "040011": "Atendimento/acompanhamento em saude do idoso",
    "040012": "Atendimento/acompanhamento de queimados",
    "040013": "Atendimento/acompanhamento de diagnostico de doencas endocrinas/metabolicas e nutricionais",
    "040014": "Tratamento de doencas do sistema nervoso central e periferico",
    "040015": "Tratamento de doencas do aparelho da visao",
    "040016": "Tratamento em oncologia",
    "040017": "Nefrologia",
    "040018": "Tratamentos odontologicos",
    "040019": "Cirurgia do sistema nervoso central e periferico",
    "040020": "Cirurgias de ouvido, nariz e garganta",
    "040021": "Deformidade labio-palatal e cranio-facial",
    "040022": "Cirurgia do aparelho da visao",
    "040023": "Cirurgia do aparelho circulatorio",
    "040024": "Cirurgia do aparelho digestivo, orgaos anexos e parede abdominal(inclui pre e pos operatorio)",
    "040025": "Cirurgia do aparelho geniturinario",
    "040026": "Tratamento de queimados",
    "040027": "Cirurgia reparadora para lipodistrofia",
    "040028": "Outras cirurgias plasticas/reparadoras",
    "040029": "Cirurgia orofacial",
    "040030": "Sequenciais",
    "040031": "Cirurgias em nefrologia",
    "040032": "Transplantes de orgaos, tecidos e celulas",
    "040033": "Medicamentos para transplante",
    "040034": "OPM auditivas",
    "040035": "OPM em odontologia",
    "040036": "OPM em queimados",
    "040037": "OPM em nefrologia",
    "040038": "OPM para transplantes",
    "040039": "Incentivos ao pre-natal e nascimento",
    "040040": "Incentivo ao registro civil de nascimento",
    "040041": "Central Nacional de Regulacao de Alta Complexidade (CNRAC)",
    "040042": "Reguladores de Atividade hormonal - Inibidores de prolactina",
    "040043": "Politica Nacional de Cirurgias Eletivas",
    "040044": "Redesignacao e Acompanhamento",
    "040045": "Projeto Olhar Brasil",
    "040046": "Mamografia para Rastreamento",
    "040047": "Projeto Olhar Brasil - Consulta",
    "040048": "Projeto Olhar Brasil - oculos",
    "040049": "Implementar Cirg. CV Pediatrica",
    "040050": "Cirurgias Eletivas - Componente I",
    "040051": "Cirurgias Eletivas - Componente II",
    "040052": "Cirurgias Eletivas - Componente III",
    "040053": "Protese Mamaria - Exames",
    "040054": "Protese Mamaria - Cirurgia",
    "040055": "Transplante - Histocompatibilidade",
    "040056": "Triagem Neonatal",
    "040057": "Controle de qualidade do exame citopatologico do colo de utero",
    "040058": "Exames do Leite Materno",
    "040059": "Atencao as Pessoas em Situacao de Violencia Sexual",
    "040060": "Sangue e Hemoderivados",
    "040061": "Mamografia para rastreamento em faixa etaria recomendada",
    "040062": "Doencas Raras",
    "040063": "Cadeiras de Rodas",
    "040064": "Sistema de Frequencia Modulada Pessoal-FM",
    "040065": "Medicamentos em Urgencia",
    "040066": "Cirurgias Eletivas - Componente unico",
    "040067": "Atencao Especializada em Saude Auditiva",
    "040068": "Terapias Especializadas em Angiologia",
    "050000": "Incentivo - MAC",
    "060000": "Media e Alta Complexidade (MAC)",
    "070000": "Vigilancia em Saude",
    "080000": "Gestao do SUS"
}

FINANC = {
    "01": "Atencao Basica (PAB)",
    "02": "Assistencia Farmaceutica",
    "04": "FAEC",
    "05": "Incentivo - MAC",
    "06": "Media e alta complexidade (MAC)",
    "07": "Vigilancia em Saude",
    "00": "Nao discriminado"
}

COMPLEX = {
    "01": "Atencao Basica",
    "02": "Media complexidade",
    "03": "Alta complexidade"
}

VINCPREV = {
    "1": "Autonomo",
    "2": "Desempregado",
    "3": "Aposentado",
    "4": "Nao segurado",
    "5": "Empregado",
    "6": "Empregador",
    "0": "Nao classificado"
}

MARCA_UCI = {
    "00": "Nao utilizou UCI",
    "01": "Unidade de cuidados intermed neonatal convencional",
    "02": "Unidade de cuidados intermed neonatal canguru ",
    "03": "Unidade intermediaria neonatal",
    "88": "Utilizou dois tipos de leitos UCI"
}

MARCA_UTI = {
    "00": "Nao utilizou UTI",
    "01": "Utilizou mais de um tipo de UTI",
    "74": "UTI adulto - tipo I",
    "75": "UTI adulto - tipo II",
    "76": "UTI adulto - tipo III",
    "77": "UTI infantil - tipo I",
    "78": "UTI infantil - tipo II",
    "79": "UTI infantil - tipo III",
    "80": "UTI neonatal - tipo I",
    "81": "UTI neonatal - tipo II",
    "82": "UTI neonatal - tipo III",
    "83": "UTI de queimados",
    "85": "UTI coronariana tipo II - UCO tipo II",
    "86": "UTI coronariana tipo III - UCO tipo III",
    "99": "UTI Doador"
}

def generate_id(row):
    hash = hashlib.md5()
    hash.update(row["NASC"].encode())
    hash.update(row["SEXO"].encode())
    hash.update(row["RACA_COR"].encode())
    return hash.hexdigest()

def normalize_nasc(nasc):
    if len(nasc) != 8:
        return nasc
    year = nasc[0:4]
    month = nasc[4:6]
    day = nasc[6:8]
    return day + month + year

def enrich(row):
    row["SEXO"] = SEXO.get(row['SEXO'], row['SEXO'])
    row["IDENT"] = IDENT.get(row['IDENT'], row['IDENT'])
    row["GESTAO"] = GESTAO.get(row['GESTAO'], row['GESTAO'])
    row["MORTE"] = MORTE.get(row['MORTE'], row['MORTE'])
    row["INSTRU"] = INSTRU.get(row['INSTRU'], row['INSTRU'])
    row["RACA_COR"] = RACA_COR.get(row['RACA_COR'], row['RACA_COR'])
    row["REGCT"] = REGCT.get(row['REGCT'], row['REGCT'])
    row["FAEC_TP"] = FAEC_TP.get(row['FAEC_TP'], row['FAEC_TP'])
    row["FINANC"] = FINANC.get(row['FINANC'], row['FINANC'])
    row["COMPLEX"] = COMPLEX.get(row['COMPLEX'], row['COMPLEX'])
    row["VINCPREV"] = VINCPREV.get(row['VINCPREV'], row['VINCPREV'])
    row["MARCA_UCI"] = MARCA_UCI.get(row['MARCA_UCI'], row['MARCA_UCI'])
    row["MARCA_UTI"] = MARCA_UTI.get(row['MARCA_UTI'], row['MARCA_UTI'])
    row["NASC"] = normalize_nasc(row['NASC'])
    row["IDENTIFICACAO"] = generate_id(row)
    return row

def clean(str):
    return str.replace('\"', '').replace("\n", "").replace("\x00", "")

def to_dict(first_line, line):
    columns = first_line.split(",")
    values = line.split(",")
    result = {}
    for i in range(len(columns)):
        # if i < len(values):
        result[clean(columns[i])] = clean(values[i])
    return result

def map(filename):
    with open(filename, 'rb') as csv_in, open('e_' + filename, 'w') as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=FIELDNAMES, extrasaction='ignore')
        writer.writeheader()

        csv_in = csv_in.read().decode("utf-8", 'ignore')
        lines = csv_in.split("\n")
        first_line = lines[0]
        for i in range(1, len(lines)):
            line = lines[i]
            if len(line.strip()) > 0:
                row = to_dict(first_line, line)
                writer.writerow(enrich(row))

def main():
    map(sys.argv[1])

if __name__ == "__main__":
    main()