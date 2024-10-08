# -*- coding: utf-8 -*-
"""Teste de Hipóteses_semana14

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10Gz8_srMiAdtzGTbHZQbMEP8OtNHGAOL
"""

#biblioteca
import pandas as pd
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, ttest_1samp, ttest_ind
import seaborn as sns

df_paciente = pd.read_csv('pacientes.csv')
df_teste = pd.read_csv('experimento_teste_ab.csv')

#conhecendo o df

df_teste.info()
df_paciente.info()

df_teste.head(10)
df_paciente.head(5)

df_teste.describe()

"""# 1- Qual dos cenários tem a maior taxa de conversão?"""

# Cenario A
total_conversões_A = df_teste[df_teste['Versão_Página'] == 'A']['Conversões'].sum()
total_visualizacao_A = df_teste[df_teste['Versão_Página'] == 'A']['Visualizações'].sum()
taxa_conversao_A =total_conversões_A /total_visualizacao_A

#Cenario B
total_conversões_B = df_teste[df_teste['Versão_Página'] == 'B']['Conversões'].sum()
total_visualizacao_B = df_teste[df_teste['Versão_Página'] == 'B']['Visualizações'].sum()
taxa_conversao_B =total_conversões_B /total_visualizacao_B

if taxa_conversao_A> taxa_conversao_B:
  print('Cenário A tem a maior taxa de conversão', taxa_conversao_A,taxa_conversao_B)
else:
  print('Cenário B tem a maior taxa de conversão', taxa_conversao_A,taxa_conversao_B)

"""#2- Calcule qual o tamanho da amostra necessária para o desenvolvimento de um teste A/B, seguindo os seguintes critérios:
#a. O cenário A, da base, como o inicial, que funciona hoje.
# b. Considere 95% de confiança de que o efeito na conversão.
"""

import scipy.stats as stats

# Parâmetros
p_A = taxa_conversao_A   # Taxa de conversão esperada para o cenário A (atual)
p_B = taxa_conversao_B + 0.10  # Taxa de conversão esperada para o cenário B (novo) com aumento de 10%
alpha = 0.05  # Nível de significância
confianca = 0.95  # Nível de confiança
beta = 0.20  # Poder do teste (1 - beta = 80%)
d = 0.10  # Diferença mínima detectável na taxa de conversão

# Valores críticos do Z-score
Z_alpha_2 = stats.norm.ppf(1 - alpha/2)
Z_beta = stats.norm.ppf(1 - beta)

# Tamanho da amostra
n= variancia da amostra_A *z_alpha + z_beta **2 /delta**2
n = (2 * (Z_alpha_2 + Z_beta)**2 * (p_A * (1 - p_A) + p_B * (1 - p_B))) / d**2
print("Tamanho da amostra necessário para cada grupo:", round(n))

"""# 3-Considerando uma amostra de 45 números que representam o index do dataframe, índices= ([909, 751, 402, 400, 726, 39, 184, 269, 255, 769, 209, 715, 677, 381, 793, 697, 89, 280, 232, 756, 358, 36, 439, 768, 967, 699, 473, 222, 89, 639, 883, 558, 757, 84, 907, 895, 217, 224, 311, 348,146, 505, 273, 957, 362]). Considerando essa amostra é possível dizerque a idade média das pessoas com problemas cardíacos é maior que 50 anos? Nível de significância igual a 5%.

"""

import numpy as np
from scipy import stats


indices_fornecidos = [909, 751, 402, 400, 726, 39, 184, 269, 255, 769, 209, 715, 677, 381, 793, 697, 89, 280, 232, 756, 358, 36, 439, 768, 967, 699, 473, 222, 89, 639, 883, 558, 757, 84, 907, 895, 217, 224, 311, 348, 146, 505, 273, 957, 362]

pacientes_correspondentes = df_paciente.iloc[indices_fornecidos]['Idade']

# Teste t de uma amostra
alpha = 0.05
t_stat, p_value = stats.ttest_1samp(pacientes_correspondentes, 50)

# Verificar se a média é maior que 50
if p_value < alpha and t_stat > 0:
    print("Rejeitamos a hipótese nula. A idade média das pessoas com problemas cardíacos é maior que 50 anos.")
else:
    print("Não rejeitamos a hipótese nula. Não há evidências suficientes para afirmar que a idade média das pessoas com problemas cardíacos é maior que 50 anos.")
print(p_value)

"""4- Quando dividimos os conjuntos em pessoas com condições de saúde adicionais e pessoas saudáveis, estaríamos lidando com amostras independentes. Isso porque os indivíduos em um grupo não têm relação direta com os indivíduos no outro grupo.

# 5-Agora considere o um conjunto de pessoas aleatória que representam
#o index do dataframe, índices = ([690, 894, 67, 201, 364, 19, 60, 319,
#588, 643, 855, 623, 530, 174, 105, 693, 6, 462, 973, 607, 811, 346, 354, 966, 943, 372]), podemos dizer que a pressão arterial média para
#pacientes com condições de saúde adicionais é igual à pressão arterial
#média para pacientes sem condições adicionais de saúde? Considere o
#nível de significância a 6%
"""

indices = ([690, 894, 67, 201, 364, 19, 60, 319,
588, 643, 855, 623, 530, 174, 105, 693, 6, 462, 973, 607, 811, 346, 354, 966, 943, 372])

pressao_com_condicoes = df_paciente.loc[indices][df_paciente['Nome_Estado_Saude'] == 'Com condições de saúde adicionais']['Pressao_Arterial']
pressao_sem_condicoes = df_paciente.loc[indices][df_paciente['Nome_Estado_Saude'] == 'Saudável']['Pressao_Arterial']

alpha = 0.06  # Nível de significância
t_stat, p_value = stats.ttest_ind(pressao_com_condicoes, pressao_sem_condicoes)

# Verificar se rejeitamos a hipótese nula
if p_value < alpha:
    print("Rejeitamos a hipótese nula. Há uma diferença significativa entre a pressão arterial média para pacientes com condições adicionais de saúde e pacientes sem condições adicionais de saúde.", t_stat, p_value)
else:
    print("Não rejeitamos a hipótese nula. Não há evidências suficientes para afirmar que há uma diferença significativa entre a pressão arterial média para pacientes com condições adicionais de saúde e pacientes sem condições adicionais de saúde.",t_stat, p_value)

"""# 6-Existe uma diferença significativa na pressão arterial média entre diferentes grupos étnicos nesta população? (Teste ANOVA, alpha é 5%)  
a. Hipótese Nula (H0): A pressão arterial média é a mesma em todos os grupos étnicos.
b. Hipótese Alternativa (H1): Há uma diferença significativa na pressão arterial média entre pelo menos dois grupos étnicos nesta população.
"""

# Calculando a média de Pressao Arterial para cada Etnia
media_formula_1 = df_paciente[df_paciente['Nome_Etnia'] == 'Afro-americano']['Pressao_Arterial'].mean()
media_formula_2 = df_paciente[df_paciente['Nome_Etnia'] == 'Asiático']['Pressao_Arterial'].mean()
media_formula_3 = df_paciente[df_paciente['Nome_Etnia'] == 'Hispânico']['Pressao_Arterial'].mean()
# Imprimindo as médias
print(f'Média de Pressao Arterial da Fórmula 1: {media_formula_1:.2f}')
print(f'Média de Pressao Arterial da Fórmula 2: {media_formula_2:.2f}')
print(f'Média de Pressao Arterial da Fórmula 3: {media_formula_3:.2f}')

import scipy.stats as stats

#realizar o teste de ANOVA
f_stat, p_value = stats.f_oneway(
df_paciente[df_paciente['Nome_Etnia'] == 'Afro-americano']['Pressao_Arterial'].values,
df_paciente[df_paciente['Nome_Etnia'] == 'Asiático']['Pressao_Arterial'].values,
df_paciente[df_paciente['Nome_Etnia'] == 'Hispânico']['Pressao_Arterial'].values
)

# Imprimir os resultados
print(f"Valor F: {f_stat}")
print(f"Valor p: {p_value}")


# Conclusão do teste
alpha = 0.05
if p_value < alpha:
    print("Rejeitamos a hipótese nula. Há uma diferença significativa na pressão arterial média entre pelo menos dois grupos étnicos nesta população..")
else:
    print("Não rejeitamos a hipótese nula.A pressão arterial média é a mesma em todos os grupos étnicos.")

"""6b. Existe uma associação entre a idade dos pacientes e sua pressão
arterial?
a. Hipótese Nula (H0): A idade dos pacientes é independente da
pressão arterial.
b. Hipótese Alternativa (H1): A idade dos pacientes está associada à
sua pressão arterial.

* **Regressão Linear.**
"""

import statsmodels.api as sm

Idade = df_paciente['Idade']
pressao_arterial=df_paciente['Pressao_Arterial']
# Adicionando uma constante aos dados de idade
idade_com_constante = sm.add_constant(Idade)

# Criando e ajustando o modelo de regressão linear com interceptação
modelo = sm.OLS(pressao_arterial, idade_com_constante).fit()

# Imprimindo os resultados
print(modelo.summary())

apha = 0.05

if modelo.pvalues['Idade']  < 0.05:
    # Se o coeficiente de interação for significativo
  if modelo.params['idade']> 0:
    print(" A idade dos pacientes está associada à sua pressão arterial e é positiva.")
  else:
    print("A idade dos pacientes está associada à sua pressão arterial e é negativa.")
else:
  print("Não rejeitamos a hipótese nula.A idade dos pacientes é independente da pressão arterial." )

"""* **Coeficiente de correlação de Pearson entre a idade dos pacientes e sua pressão arterial.**



"""

from scipy.stats import pearsonr
# Calcular o coeficiente de correlação de Pearson
coef_corr, p_valor = pearsonr(Idade, pressao_arterial)

# Imprimir o resultado
print("Coeficiente de correlação de Pearson:", coef_corr)
print("Valor-p:", p_valor)

# Conclusão do teste
alpha = 0.05
if p_valor < alpha:
    print("Rejeitamos a hipótese nula.A idade dos pacientes está associada à sua pressão arterial. ")
else:
    print("Não rejeitamos a hipótese nula.A idade dos pacientes é independente da pressão arteria.")

"""# 9. Qual é o intervalo de confiança para a média da pressão arterial entre os pacientes com condições de saúde adicionais? (nível de confiança 95%)"""

from scipy.stats import t
# Tamanho da amostra
pressao_arterial_condicoes_adicionais = df_paciente[df_paciente['Nome_Estado_Saude']=='Com condições de saúde adicionais'].count()
n = len(pressao_arterial_condicoes_adicionais)
#Desvio padrão
desvio_padrao_pressao_arterial = pressao_arterial_condicoes_adicionais.std()

#
media_pressao_arterial = pressao_arterial_condicoes_adicionais/n
# Nível de confiança
confianca = 0.95

# Graus de liberdade
graus_liberdade = n - 1

# Valor crítico da distribuição t de Student
valor_critico = t.ppf((1 + confianca) / 2, graus_liberdade)

# Margem de erro
margem_erro = valor_critico *(desvio_padrao_pressao_arterial / np.sqrt(n))

# Intervalo de confiança
intervalo_confianca = (media_pressao_arterial - margem_erro, media_pressao_arterial + margem_erro)

# Imprimir o resultado
print("Intervalo de confiança para a média da pressão arterial:", intervalo_confianca)

"""# 10. A distribuição da pressão arterial na população segue uma distribuição normal?
a. Hipótese Nula (H0): A distribuição da pressão arterial na população segue uma distribuição normal.
b. Hipótese Alternativa (H1): A distribuição da pressão arterial na população não segue uma distribuição normal.

* **Teste de Shapiro-Wilk.**
"""

from scipy.stats import shapiro

pressao =df_paciente['Pressao_Arterial'].values
stat_shapiro, p_valor_shapiro = shapiro(pressao)

# Imprimir o resultado
print("Estatística de teste de Shapiro-Wilk:", stat_shapiro)
print("Valor-p:", p_valor_shapiro)

# Verificar o resultado do teste
if p_valor_shapiro < 0.05:
    print("Não rejeitamos a hipótese nula. A distribuição parece ser normal.")
else:
    print("Rejeitamos a hipótese nula. A distribuição não parece ser normal.")