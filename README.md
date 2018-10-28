# datasus_map_csv [![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/greatjapa/datasus_map_csv/blob/master/LICENSE)

`datasus_map_csv` é composto de scripts Python que enriquecem um dado `csv` oriundo da conversão feita pelo [dbc2csv](https://github.com/greatjapa/dbc2csv). Basicamente, o fluxo consiste ler um determinado `csv` e gerar um `csv enriquecido` de acordo com o formato do dado.

## Como instalar?

Para usar o `datasus_map_csv` é preciso ter os seguintes programas instalados na sua máquina:
- git
- python3

Logo em seguinda execute os passos abaixo:

```bash
$ git clone https://github.com/greatjapa/datasus_map_csv.git
$ cd datasus_map_csv
```

## Como converter?

### Dados de de nascimento ou arquivos `sinasc`: 

```bash
$ python3 sinasc.py DNPR2016.csv
```
A conversão acima gera, por exemplo, o arquivo `e_DNPR2016.csv`.

### Dados de mortalidade ou arquivos `sim`: 

```bash
$ python3 sim.py DOPR2016.csv
```
A conversão acima gera, por exemplo, o arquivo `e_DOPR2016.csv`.

### Critérios de enriquecimento

Todas as conversões possuem executam 2 passos:
1. Remover colunas 
```
Colunas que não possuem descrição na documentação do DATASUS serão removidas.
```
2. Desnormalizar valores das colunas, por exemplo
```
Os valores atribuídos a coluna sexo (0, 1 e 2) serão substituídos pelos seus respectivos
signficados (ignorado, masculino e feminino). O mesmo ocorre para outras colunas como, por exemplo,
escolaridade, raça, fonte, local, etc
```

