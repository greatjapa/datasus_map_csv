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

```python
$ python3 sinasc.py DNPR2016.csv
```
A conversão acima gera, por exemplo, o arquivo `e_DNPR2016.csv`.

### Dados de mortalidade ou arquivos `sim`: 

```python
$ python3 sim.py DOPR2016.csv
```
A conversão acima gera, por exemplo, o arquivo `e_DOPR2016.csv`.
