# Estudo dos dados do Paraná

Até o presente momento estamos trabalhando com o seguinte modelo de dados para `SIM` e `SIHSUS`:

| COLUNAS (SIM) | Descrição                                                   |
|---------------|-------------------------------------------------------------|
| ID            | identificador sequencial da tabela                          |
| ID_INTEGRACAO | hash composta por DTNASC, SEXO, RACACOR, CODMUNRES, DTOBITO |
| SEXO          | sexo                                                        |
| RACACOR       | raça                                                        |
| DTNASC        | data de nascimento                                          |
| CODMUNRES     | municipio de residencia                                     |
| DTOBITO       | data de obito                                               |
| LOCOCOR       | local do obito                                              |
| CAUSABAS      | causa da morte                                              |

| COLUNAS (SIHSUS) | Descrição                                                   |
|------------------|-------------------------------------------------------------|
| ID               | identificador sequencial da tabela                          |
| ID_INTEGRACAO    | hash composta por NASC, SEXO, RACA_COR, MUNIC_RES, DT_SAIDA |
| ID_ATENDIMENTO   | hash composta por NASC, SEXO, RACA_COR, MUNIC_RES, CEP      |
| SEXO             | sexo                                                        |
| RACA_COR         | raça                                                        |
| NASC             | data de nascimento                                          |
| MUNIC_RES        | municipio de residencia                                     |
| CEP              | cep                                                         |
| DT_INTER         | data da internação                                          |
| DT_SAIDA         | data de saída da internação                                 |
| DIAG_PRINC       | diagnostico principal do atendimento                        |

## Mortalidade (SIM)

Os dados obtidos são do ano de 2016 e, ao todo, somam `74740` registros, dentre os quais, removemos registros que possuiam valores ruins para nossa análise. São eles:

| SIM (Dados removidos)  |   Valores  |
|------------------------|------------|
| SEXO                   | "Ignorado" |
| RACACOR                |     ""     |
| DTNASC                 |     ""     |

Isso resultou em uma base com `73327` registros minimamente válidos. Abaixo algumas estatísticas:

| SIM (SEXO)    | Valores |
|---------------|---------|
| "Masculino"   | 41773   |
| "Feminino"    | 31554   |

| SIM (RACACOR) | Valores |
|---------------|---------|
| "Branca"      | 59667   |
| "Parda"       | 10004   |
| "Preta"       | 2791    |
| "Amarela"     | 742     |
| "Indigena"    | 123     |

| SIM (TOP 5 CODMUNRES) | Valores |
|-----------------------|---------|
| "Curitiba"            | 10495   |
| "Londrina"            | 3629    |
| "Ponta Grossa"        | 2337    |
| "Maringá"             | 2142    |
| "Cascavel"            | 1733    |

| SIM (LOCOCOR)       | Valores |
|---------------------|---------|
| "Hospital"          | 48222   |
| "Domicilio"         | 16078   |
| "Outro estab saude" | 3477    |
| "Via Publica"       | 3296    |
| "Outros"            | 2239    |
| "Ignorado"          | 15      |

| SIM (TOP 5 CAUSABAS)                                | Valores |
|-----------------------------------------------------|---------|
| "I21.9 Infarto agudo do miocardio NE"               |  4849   |
| "J18.9 Pneumonia NE"                                |  2758   |
| "I64   Acid vasc cerebr NE como hemorrag isquemico" |  2717   |
| "C34.9 Bronquios ou pulmoes NE"                     |  1626   |
| "I10   Hipertensao essencial"                       |  1582   |

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

