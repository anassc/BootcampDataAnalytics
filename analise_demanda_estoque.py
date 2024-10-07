# -*- coding: utf-8 -*-
"""Analise_Demanda_Estoque.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YaNqoaosYkj4MPL-tXrQaFvtFhTBzszN

# Analise de Demanda

Imagine que trabalhamos em uma industria de calçados e queremos analisar a distribuição do estoque das lojas.

Objtivos:
1. Ler a base de dados utilizar os principios da analise exploratoria de dados visto anteriormente.

2. Analisar a distribuição do estoque e verificar se ela se assemelha a alguma distribuição conhecida.

3. Calcular qual seria a amostra necessária para estimarmos a media do estoque de cada uma das lojas com margem de erro de 2% e 10% e nivel de significancia de 5%

Antes de comecarmos vamos fazer a leitura dos pacotes necessários
"""

### para manipulação dos dados em python
import pandas as pd
import numpy as np

### para visualizacao de dados
import seaborn as sns
import matplotlib.pyplot as plt

"""
### 1. Leitura e análise exploratória dos dados"""

### leitura dos dados csv
df = pd.read_csv("/content/estoque.csv", sep = ";")

### verificando as 5 primeiras linhas dos dados
df.head(5)

### verificando os tipos dos dados encontrados
df.dtypes

### vamos converter da data para o tipo data
df["data"] = pd.to_datetime(df["data"])

### verificando novamente os tipos dos dados encontrados
df.dtypes

### rodando um describe para obter as frequencias e medidas das variáveis numéricas
df.describe()

"""Pelo describe acima vemos que temos na base o estoque e a data de medição de 3 lojas da empresa de calçados

vamos agora analisar alguns dados por loja
"""

df.groupby(["id_loja"]).agg({"estoque": [np.mean, np.min, np.max, np.std], "data": [np.min, np.max]})

"""Pela tabela acima, vemos que:
-  A loja 3 tem uma média maior de estoque do que as outras lojas e desvio padráo menor, proximo a 5.
- A loja 2 possui uma média menor de estoque e desvio padrão proximo a 6
- A loja 1 possui média de apx 180 calçados e maior desvio padrão, apx 9.7

Vamos agora analisar o histograma da distribuicão do estoque por loja

### 2. Analise da distribuição do estoque por loja
"""

numero_lojas =  df.id_loja.nunique() ### numero de lojas
numero_lojas

#### setando a paleta de cores
sns.set_palette("icefire")

numero_lojas =  df.id_loja.nunique()
fig, ax = plt.subplots(nrows=1, ncols=numero_lojas, figsize=(12, 5))
i = 0
for loja in df.id_loja.unique():
  ### histograma
  sns.set(style="darkgrid")
  sns.histplot(df[df.id_loja == loja]["estoque"], ax=ax[i], kde=True, edgecolor=None)
  ax[i].set_title('Distribuição do Estoque Diário Loja {}'.format(loja))
  ax[i].set_xlabel('Estoque Diário')
  ax[i].set_ylabel('Contagem')
  ### adiciona contador
  i = i + 1

plt.tight_layout()
plt.show()

"""Podemos ver que todos os estoques das lojas apresentam uma distribuição em formato de sino, que se assemelha muito visualmente a distribuição normal.
A loja 1 porém apresenta uma assimetria na distribuição do estoque para a esquerda.

Alternativamente, poderiamos analisar em um unico gráfico
"""

sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x="estoque", hue="id_loja", bins = 40,kde=True, palette=sns.color_palette("icefire", n_colors=3))
plt.title(label= "Distribuição do estoque por loja")
plt.show()

# Plotamos um gráfico Boxplot com a mesma paleta de cores
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='estoque', x='id_loja', palette=sns.color_palette("icefire", n_colors=3))
plt.title('Boxplot da Estoque por Loja')
plt.show()

"""Podemos perceber que o estoque da loja 3 é bem maior do que o das outras lojas e não existe overlap de estoques entre tais lojas. o que pode ser um indicativo de que:
1. As lojas apresentam compartamento de consume bem diferente, podendo estar localizadas em regioes ou pontos de venda diferentes
2. A loja 3 supostamente deve ser a que mais vende, necessitando assim de um maior estoque

## 3. Calcular qual seria a amostra necessária para estimarmos a média do estoque de cada uma das lojas

Para calcular a amostra necessária para compararmos a média do estoque de duas lojas vamos precisar da formula da margem de erro para médias em que o desvio padrao é desconhecido, vamos verificar antes o tamanho da amostra que temos para decidir qual formula utilizar
"""

df[["id_loja","estoque"]].groupby("id_loja").count()

"""Como temos 58 informações de estoque de cada uma das lojas podemos utilizar a aproximação de sigma = amplitude/4 ou sigma ou assumir que sigma é igual ao desvio padrão amostral

Assumindo o primeiro caso precisaremos da seguinte fórmula:

![image.png](data:image/png;base64,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)

E seus respectivos inputs
- sigma ': estimado a partir da amplitude, portante necessitaremos os valores max, min do estoque de cada loja para dividir essa diferença por 4
- n é o que queremos descobrir
- z(a/2) é o valor da estatistica z para o nível de significancia a assumindo que a distribuição é bicaldal.

Vamos primeiramente obter os inputs da fórmula para depois substituirmos os valores.

1. Primeira Loja
"""

##### INPUTS LOJA 1

#### sigma estimado com a amplitude
sigma_linha = (df[df.id_loja == 1]["estoque"].max() - df[df.id_loja == 1]["estoque"].min())/4


#### valor de z(a/2) para a = 5%
from scipy.stats import norm #### pacote necessário

a = 0.05
z = norm.ppf(1-a/2)

### n = ((z*sigma_linha)/me)**2

### margem , me = 2%
me = 0.02
n = round(((z*sigma_linha)/me)**2,0)
print("O tamanho da amostra será de "+str(n)+" para margem de erro de 2% e 5% de significancia")
me = 0.1 ### para margem de erro de 10%
n = round(((z*sigma_linha)/me)**2,0)
print("O tamanho da amostra será de "+str(n)+" para margem de erro de 10% e 5% de significancia")

"""2. Todas as lojas"""

#### valor de z(a/2) para a = 5%
from scipy.stats import norm #### pacote necessário

a = 0.05
z = norm.ppf(1-a/2)

for loja in df.id_loja.unique():
  sigma_linha = (df[df.id_loja == loja]["estoque"].max() - df[df.id_loja == loja]["estoque"].min())/4

  ### n = ((z*sigma_linha)/me)**2

  ### margem 2% , me = 2%
  me = 0.02
  n = round(((z*sigma_linha)/me)**2,0)
  print("O tamanho da amostra será de "+str(n)+" para margem de erro de 2% e 5% de significancia para a loja "+str(loja))
  ##margem 10% , me = 10%
  me = 0.1
  n = round(((z*sigma_linha)/me)**2,0)
  print("O tamanho da amostra será de "+str(n)+" para margem de erro de 10% e 5% de significancia para a loja "+str(loja))

"""Utilizando a estimação de sigma com a segunda opção (assumindo que o desvio padrao amostral = populacional)"""

#### valor de z(a/2) para a = 5%
from scipy.stats import norm #### pacote necessário

a = 0.05
z = norm.ppf(1-a/2)

for loja in df.id_loja.unique():
  sigma_linha = df[df.id_loja == loja]["estoque"].std()

  ### n = ((z*sigma_linha)/me)**2

  ### margem 2% , me = 2%
  me = 0.02
  n = round(((z*sigma_linha)/me)**2,0)
  print("O tamanho da amostra será de "+str(n)+" para margem de erro de 2% e 5% de significancia para a loja "+str(loja))
  ##margem 10% , me = 10%
  me = 0.1
  n = round(((z*sigma_linha)/me)**2,0)
  print("O tamanho da amostra será de "+str(n)+" para margem de erro de 10% e 5% de significancia para a loja "+str(loja))

