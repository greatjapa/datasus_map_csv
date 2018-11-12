# Estudo dos dados do Paraná

Até o presente momento estamos trabalhando com o seguinte modelo de dados para `SIM` e `SIHSUS`:

| COLUNAS (SIM) | Descrição                                                                |
|---------------|--------------------------------------------------------------------------|
| ID            | identificador sequencial da tabela                                       |
| ID_INTEGRACAO | hash composta por DTNASC, SEXO, RACACOR, CODMUNRES, DTOBITO, "Com obito" |
| SEXO          | sexo                                                                     |
| RACACOR       | raça                                                                     |
| DTNASC        | data de nascimento                                                       |
| CODMUNRES     | municipio de residencia                                                  |
| DTOBITO       | data de obito                                                            |
| LOCOCOR       | local do obito                                                           |
| CAUSABAS      | causa da morte                                                           |

| COLUNAS (SIHSUS) | Descrição                                                          |
|------------------|--------------------------------------------------------------------|
| ID               | identificador sequencial da tabela                                 |
| ID_INTEGRACAO    | hash composta por NASC, SEXO, RACA_COR, MUNIC_RES, DT_SAIDA, MORTE |
| ID_ATENDIMENTO   | hash composta por NASC, SEXO, RACA_COR, MUNIC_RES, CEP             |
| SEXO             | sexo                                                               |
| RACA_COR         | raça                                                               |
| NASC             | data de nascimento                                                 |
| MUNIC_RES        | municipio de residencia                                            |
| CEP              | cep                                                                |
| DT_INTER         | data da internação                                                 |
| DT_SAIDA         | data de saída da internação                                        |
| DIAG_PRINC       | diagnostico principal do atendimento                               |
| MORTE            | indica se o atendimento resultou em uma morte                      |

## Mortalidade (SIM)

Os dados obtidos são do ano de 2016 e, ao todo, somam `74740` registros, dentre os quais, removemos registros que possuiam valores ruins para nossa análise. São eles:

| SIM (Dados removidos)  |                Valores                          |
|------------------------|-------------------------------------------------|
| SEXO                   |              "Ignorado"                         |
| RACACOR                |                 ""                              |
| DTNASC                 |                 ""                              |
| LOCOCOR                | "Domicilio", "Via Publica", "Outros", "Ignorado"|


Isso resultou em uma base com `51699` registros minimamente válidos. Abaixo algumas estatísticas:

| SIM (SEXO)    | Valores |
|---------------|---------|
| "Masculino"   | 27871   |
| "Feminino"    | 23828   |

| SIM (RACACOR) | Valores |
|---------------|---------|
| "Branca"      | 42356   |
| "Parda"       | 6820    |
| "Preta"       | 1915    |
| "Amarela"     | 549     |
| "Indigena"    | 59      |

| SIM (TOP 5 CODMUNRES) | Valores |
|-----------------------|---------|
| "Curitiba"            | 7657    |
| "Londrina"            | 2823    |
| "Maringá"             | 1686    |
| "Ponta Grossa"        | 1561    |
| "Cascavel"            | 1178    |

| SIM (LOCOCOR)       | Valores |
|---------------------|---------|
| "Hospital"          | 48222   |
| "Outro estab saude" | 3477    |

| SIM (TOP 5 CAUSABAS)                                | Valores |
|-----------------------------------------------------|---------|
| "I21.9 Infarto agudo do miocardio NE"               |  2791   |
| "J18.9 Pneumonia NE"                                |  2609   |
| "I64   Acid vasc cerebr NE como hemorrag isquemico" |  2147   |
| "J44.0 Doen pulm obs cron c/inf resp ag tr resp inf"|  1322   |
| "C34.9 Bronquios ou pulmoes NE"                     |  1304   |

## Atendimento (SIHSUS)

Os dados obtidos são do ano de 2016 e, ao todo, somam `811511` registros, dentre os quais, removemos registros que possuiam valores ruins para nossa análise. São eles:

| SIHSUS (Dados removidos)  |   Valores  |
|---------------------------|------------|
| RACA_COR                  | "Ignorado" |

Isso resultou em uma base com `670749` registros minimamente válidos. Abaixo algumas estatísticas:

| SIHSUS (SEXO)     | Valores |
|-------------------|---------|
| "Masculino"       | 296719  |
| "Feminino"        | 374030  |

| SIHSUS (RACA_COR) | Valores |
|-------------------|---------|
| "Branca"          | 552935  |
| "Parda"           | 93921   |
| "Preta"           | 17341   |
| "Amarela"         | 5812    |
| "Indigena"        | 740     |

| SIHSUS (TOP 5 MUNIC_RES) | Valores |
|--------------------------|---------|
| "Curitiba"               | 82649   |
| "Londrina"               | 31638   |
| "Maringá"                | 21975   |
| "Ponta Grossa"           | 19433   |
| "São José dos Pinhais"   | 16708   |

| SIHSUS (TOP 5 DIAG_PRINC)            | Valores |
|--------------------------------------|---------|
| "O80.0 Parto espontaneo cefalico"    |  28199  |
| "J18.9 Pneumonia NE"                 |  18614  |
| "I20.0 Angina instavel"              |  16169  |
| "I50.0 Insuf cardiaca congestiva"    |  9967   |
| "I50.9 Insuf cardiaca NE"            |  9321   |

