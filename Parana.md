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

```sql
select SEXO, count(*) from sim group by SEXO order by count(*) desc;
```
| SIM (SEXO)    | Valores |
|---------------|---------|
| "Masculino"   | 27871   |
| "Feminino"    | 23828   |

```sql
select RACACOR, count(*) from sim group by RACACOR order by count(*) desc;
```
| SIM (RACACOR) | Valores |
|---------------|---------|
| "Branca"      | 42356   |
| "Parda"       | 6820    |
| "Preta"       | 1915    |
| "Amarela"     | 549     |
| "Indigena"    | 59      |

```sql
select CODMUNRES, count(*) from sim group by CODMUNRES order by count(*) desc limit 5;
```
| SIM (TOP 5 CODMUNRES) | Valores |
|-----------------------|---------|
| "Curitiba"            | 7657    |
| "Londrina"            | 2823    |
| "Maringá"             | 1686    |
| "Ponta Grossa"        | 1561    |
| "Cascavel"            | 1178    |

```sql
select LOCOCOR, count(*) from sim group by LOCOCOR order by count(*) desc;
```
| SIM (LOCOCOR)       | Valores |
|---------------------|---------|
| "Hospital"          | 48222   |
| "Outro estab saude" | 3477    |

```sql
select CAUSABAS, count(*) from sim group by CAUSABAS order by count(*) desc limit 5;
```
| SIM (TOP 5 CAUSABAS)                                | Valores |
|-----------------------------------------------------|---------|
| "I21.9 Infarto agudo do miocardio NE"               |  2791   |
| "J18.9 Pneumonia NE"                                |  2609   |
| "I64   Acid vasc cerebr NE como hemorrag isquemico" |  2147   |
| "J44.0 Doen pulm obs cron c/inf resp ag tr resp inf"|  1322   |
| "C34.9 Bronquios ou pulmoes NE"                     |  1304   |

# Sobre a coluna ID_INTEGRACAO

A coluna `ID_INTEGRACAO` foi criada com 2 finalidades:
- Identificar unicamente uma pessoa no sistema na tabela SIM
- Ser um análogo a chave estrangeira para descobrir os atendimentos que essa pessoa teve na tabela `sihsus`

Na tabela `sim`, é esperado que os valores de `ID_INTEGRACAO` sejam únicos já que uma pessoa só pode 
aparecer uma única vez nesta tabela (so se morre uma vez). Porém, 24 pessoas (das 74740) tiveram o 
mesmo valor na coluna `ID_INTEGRACAO`. São eles:

```sql
select ID_INTEGRACAO, CAUSABAS 
from sim 
where ID_INTEGRACAO in (
	select ID_INTEGRACAO 
    from sim 
    group by ID_INTEGRACAO 
    having count(*) > 1
)
order by ID_INTEGRACAO;
```

| ID_INTEGRACAO                    | CAUSABAS                                           |
|----------------------------------|----------------------------------------------------|
| 0628ce6ec7d079034b0fe7c1f7c58369 | P24.9 Sindr de aspiracao neonatal NE               |
| 0628ce6ec7d079034b0fe7c1f7c58369 | P24.9 Sindr de aspiracao neonatal NE               |
| 084018f18138f955c37a2f998c936ed3 | Q89.4 Reuniao de gemeos                            |
| 084018f18138f955c37a2f998c936ed3 | Q89.4 Reuniao de gemeos                            |
| 16812080fbf5a2fe0015e591e5cd491b | P07.3 Outr recem-nascidos de pre-termo             |
| 16812080fbf5a2fe0015e591e5cd491b | B24   Doenc p/HIV NE                               |
| 5b583286515903b617958f3ccb5b8821 | Q89.4 Reuniao de gemeos                            |
| 5b583286515903b617958f3ccb5b8821 | Q89.4 Reuniao de gemeos                            |
| 692b5275b261720c2c1c45e727c41188 | P01.0 Fet rec-nasc afet incompetencia colo uterino |
| 692b5275b261720c2c1c45e727c41188 | P01.0 Fet rec-nasc afet incompetencia colo uterino |
| 6a2360ec25115a14ba09bd8de6865e30 | P01.0 Fet rec-nasc afet incompetencia colo uterino |
| 6a2360ec25115a14ba09bd8de6865e30 | P01.0 Fet rec-nasc afet incompetencia colo uterino |
| 811dcdd82cca76b6e1a2c237e16d5233 | I69.4 Sequelas acid vasc cerebr NE c/hemorr isquem |
| 811dcdd82cca76b6e1a2c237e16d5233 | I69.4 Sequelas acid vasc cerebr NE c/hemorr isquem |
| 883c099187fbc17f09ca86b785e85606 | Q25.1 Coartacao da aorta                           |
| 883c099187fbc17f09ca86b785e85606 | P01.0 Fet rec-nasc afet incompetencia colo uterino |
| 9e0c29a2950f5d8aedebb7f9acdd3a6b | P01.5 Fet rec-nasc afetados p/gravidez mult        |
| 9e0c29a2950f5d8aedebb7f9acdd3a6b | P01.5 Fet rec-nasc afetados p/gravidez mult        |
| a02ccbd463e09fbe9468eb898dfe4c70 | I60.9 Hemorragia subaracnoide NE                   |
| a02ccbd463e09fbe9468eb898dfe4c70 | G03.9 Meningite NE                                 |
| ae79c90fccc0f65e21a09641acb3e3c4 | P00.5 Fet rec-nasc afetados p/traum materno        |
| ae79c90fccc0f65e21a09641acb3e3c4 | P00.5 Fet rec-nasc afetados p/traum materno        |
| cf42d984ee94cddb3cb62c1ee849ee58 | C34.9 Bronquios ou pulmoes NE                      |
| cf42d984ee94cddb3cb62c1ee849ee58 | C18.8 Lesao invasiva do colon                      |

## Atendimento (SIHSUS)

Os dados obtidos são do ano de 2016 e, ao todo, somam `811511` registros, dentre os quais, removemos registros que possuiam valores ruins para nossa análise. São eles:

| SIHSUS (Dados removidos)  |   Valores  |
|---------------------------|------------|
| RACA_COR                  | "Ignorado" |

Isso resultou em uma base com `670749` registros minimamente válidos. Abaixo algumas estatísticas:

```sql
select SEXO, count(*) from sihsus group by SEXO order by count(*) desc;
```
| SIHSUS (SEXO)     | Valores |
|-------------------|---------|
| "Masculino"       | 296719  |
| "Feminino"        | 374030  |

```sql
select RACA_COR, count(*) from sihsus group by RACA_COR order by count(*) desc;
```
| SIHSUS (RACA_COR) | Valores |
|-------------------|---------|
| "Branca"          | 552935  |
| "Parda"           | 93921   |
| "Preta"           | 17341   |
| "Amarela"         | 5812    |
| "Indigena"        | 740     |

```sql
select MUNIC_RES, count(*) from sihsus group by MUNIC_RES order by count(*) desc limit 5;
```
| SIHSUS (TOP 5 MUNIC_RES) | Valores |
|--------------------------|---------|
| "Curitiba"               | 82649   |
| "Londrina"               | 31638   |
| "Maringá"                | 21975   |
| "Ponta Grossa"           | 19433   |
| "São José dos Pinhais"   | 16708   |

```sql
select DIAG_PRINC, count(*) from sihsus group by DIAG_PRINC order by count(*) desc limit 5;
```
| SIHSUS (TOP 5 DIAG_PRINC)            | Valores |
|--------------------------------------|---------|
| "O80.0 Parto espontaneo cefalico"    |  28199  |
| "J18.9 Pneumonia NE"                 |  18614  |
| "I20.0 Angina instavel"              |  16169  |
| "I50.0 Insuf cardiaca congestiva"    |  9967   |
| "I50.9 Insuf cardiaca NE"            |  9321   |

```sql
select ID_ATENDIMENTO, count(*) from sihsus group by ID_ATENDIMENTO order by count(*) desc limit 5;
```
| SIHSUS (TOP 5 PESSOAS/ID_ATENDIMENTO COM MAIS ATENDIMENTOS) | VALOR |
|-------------------------------------------------------------|-------|
| "2d5e826f10b82d71d6e008135ba5f4a8"                          | 91    |
| "74666f04899379188677ce346ce0dd9b"                          | 57    |
| "2903e4e6ede51f08a7ff5b27880fe8b6"                          | 45    |
| "19cb14b0da8ea64142c3089066301e4b"                          | 42    |
| "303717e5924eb0fe0ed243c18cf7bc37"                          | 42    |

## SIM X SIHSUS

Dos `74740` registros da tabela SIM, temos `17165` que aparecem na tabela SIHSUS:
```sql
select sihsus.ID_ATENDIMENTO, sihsus.SEXO, sihsus.RACA_COR, sihsus.MUNIC_RES, sihsus.CEP, sihsus.DIAG_PRINC, sihsus.DT_INTER, sihsus.DT_SAIDA, sim.DTOBITO, sim.CAUSABAS
from sihsus
inner join sim
on sim.ID_INTEGRACAO = sihsus.ID_INTEGRACAO
order by sihsus.ID_ATENDIMENTO;
```