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

*OBS:* O número de atendimentos com morte foram `28396` dada pela query abaixo:
```sql
select count(*) from sihsus where MORTE='Com obito';
```

## SIM X SIHSUS

Como exemplo, considere a pessoa com maior número de atendimento na tabela `sihsus` e vamos ver toda seu histórico de atendimento:

```sql
select * from sihsus where ID_ATENDIMENTO='2d5e826f10b82d71d6e008135ba5f4a8' order by DT_SAIDA asc;
```

| ID_INTEGRACAO                    | ID_ATENDIMENTO                   | SEXO     | RACA_COR | NASC       | MUNIC_RES  | CEP      | DT_INTER   | DT_SAIDA   | DIAG_PRINC                                      | MORTE     |
|----------------------------------|----------------------------------|----------|----------|------------|------------|----------|------------|------------|-------------------------------------------------|-----------|
| 8d95d034920d8131e1e519a4c9a39cb4 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-02-17 | 2016-02-22 | A49.8 Outr infecc bacterianas localiz NE        | Sem obito |
| d438376753ab40af2d636640f0a74cf0 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-01 | 2016-04-01 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 21e9f181d559356e3cda648d9fb2d157 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-02 | 2016-04-02 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 34d3782450978b6d249e7b8d6ef135b9 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-03 | 2016-04-03 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 41b2adaf4799da7dbba20cd1658c83bd | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-04 | 2016-04-04 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| f1baefe1a670461da50da03400164d72 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-05 | 2016-04-05 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 1b622d9aae7d856c3552e377e3135ec2 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-06 | 2016-04-07 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 443cf87c7cd746c0dee6c4fded6fa400 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-08 | 2016-04-08 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 507d8514acd2305d3ad3aa2e9cd19526 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-09 | 2016-04-09 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 90f331cea8928b36deb57d8346a67323 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-10 | 2016-04-10 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 93cf43d1a58adff44ee8965c99adff23 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-11 | 2016-04-12 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| a2e4f8533d805643dd45de4299362208 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-13 | 2016-04-13 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4e2d2e2918ad0452fa44e076772d4e5f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-14 | 2016-04-14 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| a8902be6cb519d3c437548bdf55cedac | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-15 | 2016-04-16 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| aae6393a6ed628a24bb9c7422e8421af | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-17 | 2016-04-18 | K56.6 Outr form de obstrucao intestinal e as NE | Sem obito |
| 9ff0308a05b4cf9e8143b66bc40af330 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-19 | 2016-04-19 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 55bbece04f9728661f78c13fba512c62 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-20 | 2016-04-20 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| d6f5347fd372779eb8f10c194993f448 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-21 | 2016-04-23 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 54aad33b60e49878bc7a9d0eb19caca2 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-24 | 2016-04-25 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| e00f778b196dd01bfb7851e4cff32758 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-26 | 2016-04-26 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 9b53c69497e9c76e3b7dc752407606f8 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-27 | 2016-04-27 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| c3e0b8c94dea1e4772e74f9b6541d702 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-28 | 2016-04-28 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 098d0c50b9aa972e37f6bce1c532e1e8 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-29 | 2016-04-29 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| d16abf6db43460eca5eae205d2cd0842 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-04-30 | 2016-04-30 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 6208bd242eaaac6b64ccc40343650257 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-01 | 2016-05-01 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0e2b48748ed64bf7da6c5f20f2118cd7 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-02 | 2016-05-02 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 3c56a5b5d70052002fb93cbf0b28d014 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-03 | 2016-05-03 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0454f341c12111b2b808efe8a7495127 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-04 | 2016-05-04 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 11dd94dec465f83358439fb0143a5f11 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-05 | 2016-05-05 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 738b0f7aa97b81ba8f852422ed808472 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-06 | 2016-05-06 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 2bf31194c8f3cf71f02e3151f8af4649 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-07 | 2016-05-08 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| a3dc29d917d394b3b8779e8f3bad49c2 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-09 | 2016-05-09 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 9a832a0fe921ad186d47fe6157e075f1 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-10 | 2016-05-11 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 055b564fe515e1e09c5db7dae4c3dc2a | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-12 | 2016-05-12 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 40a9008e3184f01792b196f08370d23c | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-13 | 2016-05-13 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| e95d8c01ba2e374bbcc6b1edcaea4ca5 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-14 | 2016-05-14 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 2fb5929ec1e1c8368245f6958075fce0 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-15 | 2016-05-15 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| abcc9b67d1c7609e2bcdae82cec7f980 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-16 | 2016-05-16 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| af70610f28a12902c8e40f56e327b523 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-17 | 2016-05-17 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4b5103f05ca6e392325bd2c9fe2adaf1 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-18 | 2016-05-18 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 5b2f152ff871f24e62461d6094320ce8 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-19 | 2016-05-20 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 2f4d3ee8080a88ab7f72fad41ef28edf | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-21 | 2016-05-21 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| af74cd943e5ad12f5ec3c7ecc3157eff | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-22 | 2016-05-22 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| a6a40e665daef9699a435a77f9ee0497 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-23 | 2016-05-23 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 179e90e8c0b6956480d0fdeddd0d3c72 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-24 | 2016-05-24 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0a50ebca31a4214d02d27760cde9691d | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-25 | 2016-05-25 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| f86f70a2322352285d4204047279279b | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-26 | 2016-05-26 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4d7cb91dbafd768d33a4361eec09170b | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-27 | 2016-05-27 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| db8072ac812454303ebb2203a11e957a | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-28 | 2016-05-28 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 6dc70d019933edb61d425c530fa3142e | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-29 | 2016-05-29 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4a0e43d0487d1b1b444e48a88973780a | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-30 | 2016-05-30 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4fc62cbd5b2ae4207f458eee813525e9 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-05-31 | 2016-05-31 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| b61a315e04ea1ad34cddeb8c4f73dcf3 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-01 | 2016-06-01 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| f70207a4ea604dd8b8a24462ad3cdce0 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-02 | 2016-06-02 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 35a6e48819542283a05ebda2684c6547 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-03 | 2016-06-03 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 6b1d392cf35939fa823e903c0c28062f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-04 | 2016-06-04 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 60147a922922422cca7ef90b975bc736 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-05 | 2016-06-05 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 3c3b8d262e7e80561aefd7213e7abbcd | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-06 | 2016-06-06 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| eecf4d444011266618f3fac9f23186e0 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-07 | 2016-06-07 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 790ec195828ce2cdb4058e760f8e027f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-08 | 2016-06-08 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0749ddad7364a9e9b738c9d72595b0c3 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-09 | 2016-06-09 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 06395aa92c5acfdaf74ceb7d8ead151b | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-10 | 2016-06-10 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| fc064477bd3f2bdc9136b291abba7805 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-11 | 2016-06-12 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| ff82c95f2fde24b08e7fd3af81a9bb44 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-13 | 2016-06-13 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 29e67d52a923f2fd8c53c541cd7e8bb6 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-14 | 2016-06-14 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0df06a6e6d23128901834f6e57b0372e | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-15 | 2016-06-15 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0f399aadb90af7e6ab9b4959d7b0da10 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-16 | 2016-06-16 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 9ab5217e771c6e8e019fd20ac6410ca2 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-17 | 2016-06-17 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 63b01d9b5247d6a0c64495d6eac0ef6e | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-18 | 2016-06-18 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 426b6cc3eb8a5b7ccfb39b0f3e5fcd87 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-19 | 2016-06-19 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 4ec7c4e5975080d2a78818e1027007d8 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-20 | 2016-06-20 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 9f2f2ad75b169232ac7cfe4e719f047b | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-21 | 2016-06-21 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 812278b0df64a7af6cb599bc764a8196 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-22 | 2016-06-22 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| d1ee45510d35bdb16ecfe57236cead77 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-23 | 2016-06-23 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 7e68ebb65960bac94b9e702c25f93dfd | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-24 | 2016-06-24 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 0015eee4885329e6b7526a94321a0c7f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-25 | 2016-06-25 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 8a6612e3f2e7cbde4619c6ba7c74739a | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-26 | 2016-06-26 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 6eced09f45a2c348e412695a18c72b0c | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-27 | 2016-06-27 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| d09176be89cfe90c4c7d20803405bcab | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-28 | 2016-06-28 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| b86c772202f483347adee6897ab7f02f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-29 | 2016-06-29 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| d181a7d14371637fcdba2c8237da65b3 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-06-30 | 2016-06-30 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 890302cb8a6565c9b6a193e5339c6031 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-01 | 2016-07-01 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 19095dffde3727b5bd4de30237401e00 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-02 | 2016-07-04 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 64eddb0493bf3ba74db417dafbf2667f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-05 | 2016-07-05 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| afd0f86fe84d38efee5024f4eba30e11 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-06 | 2016-07-06 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 7340e9457f1f0615642df6a8d7191e6a | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-07 | 2016-07-07 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| cb926b8cd52966c93662306000a0064e | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-08 | 2016-07-08 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 37e83dca9651081acb548ed6c5b47869 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-09 | 2016-07-09 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 330f113f5f7c1b5e2dc35630a2298981 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-10 | 2016-07-10 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| 282a4ec4c54ceef5c8dd72f5f311648f | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-11 | 2016-07-14 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Sem obito |
| cd88eeda8bbad52a50b5a09453fd6bd9 | 2d5e826f10b82d71d6e008135ba5f4a8 | Feminino | Branca   | 1964-10-26 | Cerro Azul | 83570000 | 2016-07-15 | 2016-07-16 | L98.9 Afeccoes da pele e do tec subcutaneo NE   | Com obito |

Note que essa mesma pessoa morreu em seu último atendimento. Se pegarmos o `ID_INTEGRACAO` desse registro e consultarmos
a tabela `sim` teremos o seguinte valor:

```sql
select * from sim where ID_INTEGRACAO = 'cd88eeda8bbad52a50b5a09453fd6bd9';
```
| ID_INTEGRACAO                    | SEXO     | RACACOR | DTNASC     | CODMUNRES  | DTOBITO    | LOCOCOR  | CAUSABAS                              |
|----------------------------------|----------|---------|------------|------------|------------|----------|---------------------------------------|
| cd88eeda8bbad52a50b5a09453fd6bd9 | Feminino | Branca  | 1964-10-26 | Cerro Azul | 2016-07-16 | Hospital | C53.8 Lesao invasiva do colo do utero |

Outra estatistica interessante é que assim como o exemplo acima, temos outros `17165` registros da tabela `sihsus` que aparecem na tabela `sim`. Vide query abaixo:

```sql
select sihsus.ID_ATENDIMENTO, sihsus.SEXO, sihsus.RACA_COR, sihsus.MUNIC_RES, sihsus.CEP, sihsus.DIAG_PRINC, sihsus.DT_INTER, sihsus.DT_SAIDA, sim.DTOBITO, sim.CAUSABAS
from sihsus
inner join sim
on sim.ID_INTEGRACAO = sihsus.ID_INTEGRACAO
order by sihsus.ID_ATENDIMENTO;
```
