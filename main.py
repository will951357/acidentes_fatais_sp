''' Introdução '''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import geopandas as gpd
import contextily as ctx
from pathlib import Path
from pprint import pprint


# Definindo o caminho absoluto do arquivo
root_path = Path(__file__).parent
file_path = root_path / 'obitos.csv'

# Definindo o DataFrame principal
# Irá capturar os dados do .csv
main_df = pd.read_csv(file_path, encoding='latin1', delimiter=';')
pprint(main_df.head())


area =  main_df.shape   # Define o numero de linhas e colunas
info = main_df.info()     # Armazena as informações da base de dados

pprint(f'A tabela possui {area[0]} linhas e {area[1]} colunas \n\n')
print('Suas colunas são:\n')
pprint(info)

# Realizando alguns filtros para remover dados com status 'NAO DISPONIVEL'
main_df = main_df[main_df['Sexo'] != 'NAO DISPONIVEL']
main_df = main_df[main_df['Meio de locomoção da vítima'] != 'NAO DISPONIVEL']
main_df = main_df[main_df['Tipo de vítima'] != 'NAO DISPONIVEL']
main_df = main_df[main_df['Tipo de Sinistro'] != 'NAO DISPONIVEL']


#Cores
cores_hora = ['#FFD700','#FFD700','#8B0000','#FFD700','#C0C0C0']
cores_dia = ['#8B0000','#FFD700','#FFD700','#FFD700','#FFD700','#FFA500','#8B0000']
cores_genero = ['#87CEFA','#FF69B4']
cores_tipo_vitima = ["#9b59b6", "#e74c3c", "#2ecc71"]

#Paletas
paleta_tipo_veiculo = sns.color_palette("husl", 7)
paleta_degrade=sns.cubehelix_palette(8, start=2, rot=0, dark=0, light=.75, reverse=True)
paleta_hora = sns.color_palette(cores_hora)
paleta_tipo_vitima = sns.color_palette(cores_tipo_vitima)
paleta_genero = sns.color_palette(cores_genero)
paleta_dia = sns.color_palette(cores_dia)

# A analise se baseará na seguintes perguntas que tentarei responder abaixo:
# 1. Com quem ocorre
# 2. Onde ocorre
# 3. Quando ocorre
# 4. Como ocorre

# Com quem ocorre?
# Descreve as partes envolvidas no sinistro. De forma geral, considerando que temos a classificação por
# Sexo, Idade, Tipo de vítima e veículo em que estavam, podemos apresentar esses dados da seguinte forma:

# Sexo:
sexo = main_df['Sexo'].value_counts()
homens = sexo.get('MASCULINO', 0)
mulheres = sexo.get('FEMININO', 0)
total_obitos = homens + mulheres

if total_obitos > 0:
    perc_masculino = (homens / total_obitos) * 100     # Percentual de homens
    perc_feminino = (mulheres / total_obitos) * 100    # Percentual mulheres
else:
    perc_masculino = perc_feminino = 0

pprint('Homens: {} ({:.2f}%)'.format(homens, perc_masculino))
pprint('Homens: {} ({:.2f}%)'.format(mulheres, perc_feminino))

graf_sexo = plt.figure(figsize=(7,7))
sns.set_style('ticks')
plt.pie(sexo.values, labels=sexo.keys(), colors=paleta_genero, autopct='%1.1f%%')
plt.title('Vítimas por gênero', fontsize=21)

# -----------------------------------------------------------------------------------

# Acima é possivel indicar que os óbitos masculinos é maior do
# os óbitos femininos. Mas qual a faxia etária desses pessoas?

idade_homem = main_df[main_df['Sexo'] == 'MASCULINO']['Idade da vítima'].dropna().astype(int)
idade_mulher = main_df[main_df['Sexo'] == 'FEMININO']['Idade da vítima'].dropna().astype(int)

# Combinar as contagens de idades de homens e mulheres
idades_combinadas = pd.concat([idade_homem, idade_mulher])

# Encontrar a idade com o maior número de óbitos
idade_mais_obitos = idades_combinadas.value_counts().idxmax()
numero_de_obitos = idades_combinadas.value_counts().max()

# Media de idade
media_idade_homem = idade_homem.mean()
media_idade_mulher = idade_mulher.mean()

# Garantir que as colunas de idades não contenham valores NaN ou inválidos
main_df['idade_homem'] = pd.Series(dtype=int)
main_df['idade_mulher'] = pd.Series(dtype=int)

main_df.loc[main_df['Sexo'] == 'MASCULINO', 'idade_homem'] = idade_homem
main_df.loc[main_df['Sexo'] == 'FEMININO', 'idade_mulher'] = idade_mulher

# Plotar a distribuição das idades por gênero
plt.figure(figsize=(14, 7))
sns.set_style('whitegrid')

# Plotar histogramas de idades de homens e mulheres
ax = sns.histplot(idade_homem, color='#6495ED', label='Homens', binwidth=1)
ax = sns.histplot(idade_mulher, color='#FF69B4', label='Mulheres', binwidth=1)

# Configurações do gráfico
plt.xlim(10.5, 51.5)
plt.xlabel('Idade', fontsize=17)
plt.ylabel('N° de vitimas', fontsize=17)
plt.xticks(fontsize=14)
plt.yticks(fontsize=15)
plt.title('Distribuição das idades por gênero', fontsize=23)
plt.legend(title='Sexo')
plt.ylim(0, numero_de_obitos + 200)
plt.annotate(
    f'Idade {idade_mais_obitos}\n{numero_de_obitos} Vítimas',
    xy=(idade_mais_obitos, numero_de_obitos),
    xytext=(idade_mais_obitos, numero_de_obitos),
    arrowprops=dict(facecolor='grey', shrink=0.05),
    fontsize=12,
    color='grey'
)

# Adicionar textos com as médias de idades de óbitos
plt.text(
    55, numero_de_obitos, 
    f'Média idade (Homens): {media_idade_homem:.1f}',
    fontsize=12, color='blue'
)

plt.text(
    55, numero_de_obitos - 100, 
    f'Média idade (Mulheres): {media_idade_mulher:.1f}',
    fontsize=12, color='magenta'
)

# -----------------------------------------------------------------------------------------------------

# Agora devemos analisar o tipo de vítima, sendo classificado entre Condutor, Pedestre e Passageiro
vitimas = main_df['Tipo de vítima'].value_counts()
vitimas_perc = (vitimas/vitimas.sum())*100


fig, ax = plt.subplots(figsize=(10, 7))
sns.barplot(x=vitimas.index, y=vitimas.values, palette=paleta_tipo_vitima, ax=ax) # Gráfico de barras

# Configurações adicionais
plt.xlabel('Tipo de Vítima', fontsize=14)
plt.ylabel('Número de Vítimas', fontsize=17)
plt.title('Classificação das Vítimas por Tipo', fontsize=23)
sns.despine()

# _------------------------------------------------------------------------------------
# Gráfico de barras dividido por gênero
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x='Tipo de vítima', hue='Sexo', palette={'MASCULINO': '#6495ED', 'FEMININO': '#FF69B4'}, ax=ax, order=['CONDUTOR','PEDESTRE','PASSAGEIRO'])

# Configurações adicionais
plt.xlabel('Tipo de Vítima', fontsize=14)
plt.ylabel('Número de Vítimas', fontsize=17)
plt.title('Classificação das Vítimas por Tipo e Gênero', fontsize=23)
sns.despine()

# Aqui podemos observar que os condutores masculinos são mais acometidos por obitos em acidentes de transito


# ----------------------------------------------------------------------------------------------

# Respondendo a ultima pergunta 'Com quem ocorre' podemos classificar a categoria por idade e sexo
# Assim teremos uma noção maior da faixa etaria por Condutor, Pedestre e Passageiros

fig, ax = plt.subplots(figsize=(10, 7))
sns.violinplot(x='Tipo de vítima', y='Idade da vítima', hue='Sexo', palette={'MASCULINO': '#6495ED', 'FEMININO': '#FF69B4'}, data=main_df)
plt.xlim(-0.5,2.5)
plt.title('Distribuição de idade das diferentes vítimas',fontsize=19)
plt.xlabel(' ')
plt.ylabel('idade da vítima',fontsize=15)

# Esse grafico nos traz uma informação importante
# A pessoas com mais idade (mulher) são as que mais morrem como pedestre em acidente de transito.
# Já como passageiros, as pessoas mais jovens na casa dos 20-30 anos são acometidas pelo obito


# --------------------------------------------------------------------------
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Meio de locomoção da vítima'], order=main_df['Meio de locomoção da vítima'].value_counts().index, palette=paleta_tipo_veiculo)

plt.xlabel(' ')
plt.ylabel(' ')
plt.title('Veículos das vítimas',fontsize=21)
plt.xticks(fontsize=11)
plt.yticks(fontsize=13)
plt.ylabel('N° de mortes',fontsize=13)

tipo_veiculo_perc = (main_df['Meio de locomoção da vítima'].value_counts()/main_df['Meio de locomoção da vítima'].value_counts().sum()) * 100
pprint(tipo_veiculo_perc)

# Aqui podemos confirmar o que foi mostrado no grafico de tipo de vitima, os motociclistas
# equivalem a 37% dos obitos em acidentes de trânsito, seguidos de pedestres com 26% e automóvel com 24%

# -----------------------------------------------------------------
# Agora separamos novamente por genero e faixa etária

fig, ax = plt.subplots(figsize=(10, 7))
sns.boxplot(x='Meio de locomoção da vítima', y='Idade da vítima', hue='Sexo', palette={'MASCULINO': '#6495ED', 'FEMININO': '#FF69B4'}, order=main_df['Meio de locomoção da vítima'].value_counts().index, data=main_df)
plt.title('Idade das vítimas por veículo',fontsize=21)
plt.xlabel(' ')
plt.ylabel('Idade',fontsize=13)
plt.legend(title='Sexo')

# A partir desse gráfico conseguimos tirar algumas conclusões interessantes:

# Os motociclistas costumam ser mais novos que os usuários de outros veículos. Isso pode nos ajudar a explicar o alto número de morte dos jovens nos acidentes de trânsito.
# Os pedestres costumam ser mais velhos que os usuários de outros veículos. Mas ainda vemos muitos idosos (+65) morrendo de motocicletas em acidentes.



# --------------------------------------------------------------------------------
# A segunda perguta é, ONDE acontecem
# Estudar essa distribuição geográfica faz com que possamos nos localizar no conjunto de dados.

# Converter as colunas para float, garantindo que vírgulas sejam convertidas para pontos corretamente
main_df['latitude'] = main_df['latitude'].str.replace(',', '.').astype(float)
main_df['longitude'] = main_df['longitude'].str.replace(',', '.').astype(float)

# Remover valores ausentes nas colunas de latitude e longitude
main_df_filtered = main_df.dropna(subset=['latitude', 'longitude'])

# Filtrar para manter apenas coordenadas dentro da faixa esperada para São Paulo
main_df_filtered = main_df_filtered[
    (main_df_filtered['latitude'] >= -25.4383) & (main_df_filtered['latitude'] <= -19.7518) &
    (main_df_filtered['longitude'] >= -53.0288) & (main_df_filtered['longitude'] <= -44.0723)
]

# Criar um GeoDataFrame
gdf = gpd.GeoDataFrame(main_df_filtered, geometry=gpd.points_from_xy(main_df_filtered.longitude, main_df_filtered.latitude))

# Definir o sistema de referência de coordenadas (CRS) para o WGS 84
gdf.crs = {'init': 'epsg:4326'}

# Reprojetar para Web Mercator para usar com contextily
gdf = gdf.to_crs(epsg=3857)

# Criar o gráfico
fig, ax = plt.subplots(figsize=(20, 12))
gdf.plot(ax=ax, markersize=1, color='black', alpha=0.5)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Ajustar o título e esconder os eixos
plt.title('Concentração de acidentes fatais no Estado de São Paulo (2015 - 2020)', fontsize=29)
ax.set_axis_off()

# Aqui vemos que a região do centro de São Paulo e Litoral possui maior numero de acidentes fatais de transito
mortes_por_municipio = main_df['Município'].value_counts()
mortes_por_municipio_perc = (mortes_por_municipio/mortes_por_municipio.sum())*100

print(mortes_por_municipio)
print()
print(mortes_por_municipio_perc)

# ------------------------------------------------------------------------------------
# Agora que sabemos que a concetração de mortes está no centro de São Paulo, quais são as via que mais
# ocorrem esses acidentes?

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Tipo de via'], color='grey')

plt.title('Tipos de via',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')

plt.xlim(-0.5, 1.5)
plt.xticks(fontsize=13)

# As vias municipais se mostram mais perigosas do que as rodovias.
#-----------------------------------------------------------------------------------
# Agora podemos nos perguntar o seguinte. Quem mais se acidenta fatalmente, ou qual tipo de vículo estão
# mais envolvidos nesse tipo de acidente

# ------------------------------------------------------------------------------
# Numero de Mortes em Vias municipais x Rodovias por Genero
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Tipo de via'],hue='Sexo', palette={'MASCULINO': '#6495ED', 'FEMININO': '#FF69B4'})

plt.title('N° de vitimas em vias municipais X rodovias (gênero)',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xlim(-0.5, 1.5)
plt.xticks(fontsize=13)
plt.legend(title='Gênero', loc='upper right', labels=['MASCULINO', 'FEMININO'])

# Numero de Mortes em Vias municipais x Rodovias por tipo de vitima

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Tipo de via'],hue='Tipo de vítima', palette=paleta_tipo_vitima)

plt.title('N° de vitimas em vias municipais X rodovias (tipo de vítima)',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=13)
plt.legend(title='Tipo de vítima', loc='upper right', labels=['CONDUTOR', 'PASSAGEIRO','PEDESTRE'])

# Numero de Mortes em Vias municipais x Rodovias por tipo de veículo

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Tipo de via'],hue='Meio de locomoção da vítima', palette=paleta_tipo_veiculo)

plt.title('N° de vitimas em vias municipais X rodovias (tipo de veículo)',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=13)
plt.legend(title='Veículo da vítima', loc='upper right', labels=['ONIBUS', 'MOTOCICLETA','PEDESTRE','BICICLETA','CAMINHÃO','AUTOMÓVEL','OUTROS'])

# o terceiro gráfico vemos um resultado interessante. Embora o número de motociclistas tenha sido maior que o de automóveis, nas rodovias não acontece isso. O número de mortes com automóveis se mostra maior do que com motocicletas.
# Entender onde as pessoas morrem informam aos formuladores de políticas públicas onde devem atuar para reduzir os números de acidentes. Traçar planos eficientes são necessários para atacar o problema, e devemos fazer isso nos baseando em dados estatísticos.
# Agora iremos explorar a relação temporal. Estudaremos, então, quando essas mortes acontecem.

# -------------------------------------------------------------------------------
# A proxima pergunta a ser respondida é: Quando acontece?
# Pensar em problemas inclui pensar no "quando aconteceu"

mes_obito = main_df['Mês do Óbito'].value_counts().sort_index()
mes_obito_perc = mes_obito/mes_obito.sum()

turno_obito = main_df['Turno'].value_counts().sort_index()
turno_obito_perc = (turno_obito/turno_obito.sum())*100

dia_semana_obito = main_df['Dia da Semana'].value_counts().sort_index()
dia_semana_obito_perc = (dia_semana_obito/dia_semana_obito.sum())*100

# -------------------------------------------------------------------------------
# frequencia de mortes por mes
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))

df_area = pd.DataFrame({'Mês do Óbito': mes_obito.index, 'Número de Vítimas': mes_obito.values})

ax.set_xticks(df_area['Mês do Óbito'])
ax.set_xticklabels(df_area['Mês do Óbito'], rotation=45, ha='right')  # Rotacionar os rótulos para melhor legibilidade

sns.lineplot(x='Mês do Óbito', y='Número de Vítimas', data=df_area, color='black', marker='o', linewidth=2.5, linestyle='-')

plt.title('Frequência das mortes por acidentes em cada mês', fontsize=19)
plt.ylabel('N° de vítimas', fontsize=15)
plt.xlabel('Mês do Óbito', fontsize=15)  # Atualizado para mostrar o nome da coluna
plt.xticks(fontsize=13)
plt.grid(True)

# ---------------------------------------------------------------
# Dias da semana
print((dia_semana_obito_perc))

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Dia da Semana'], palette=cores_hora)

plt.title('Mortes fatais de acordo com os dias da semana',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=13)

# ---------------------------------------------------------------
# Turno do dia
print(dia_semana_obito_perc)

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(data=main_df, x=main_df['Turno'], palette=cores_hora)

plt.title('Mortes fatais de acordo com os turnos do dia',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=13)

# --------------------------------------------------------------
# Tempo de acidente até o óbito
tempo_acidente_obito = main_df['Tempo entre o Sinistro e o Óbito'].value_counts()
tempo_acidente_obito_perc = (tempo_acidente_obito/tempo_acidente_obito.sum())*100

# Aqui podemos concluir que os acidentes ocorrem, em sua maioria, nos finais de semana
# e no período noturno. Isso é importante levar em consideração para escolhas individuais
# como evitar sair nesses horários mais volumosos e politicas publicas como aumento da fiscalização
# em certos dias e horários.

# -----------------------------------------------------------
# -----------------------------------------------------------
# Como acontecem?
# A ultima pergunta a ser respondida é, como acontecem o que ajuda a responder também quais são as partes
# envolvida no sinistro.

outro_veiculo_envolvido = main_df['Outro Veículo Envolvido'].value_counts()
outro_veiculo_envolvido_perc = (outro_veiculo_envolvido/outro_veiculo_envolvido.sum())*100

tipo_sinistro = main_df['Tipo de Sinistro'].value_counts()
tipo_sinistro_perc = (tipo_sinistro/tipo_sinistro.sum())*100

print(f'Porcentagem de outros veículos envolvidos {outro_veiculo_envolvido_perc}')
print(tipo_sinistro_perc)

# --------------------------------------------------------------
# Envolvimento de outros veículos
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(15, 5))
sns.countplot(data=main_df, x=main_df['Outro Veículo Envolvido'], order=main_df['Outro Veículo Envolvido'].value_counts().index, color='black')

plt.title('Envolvimento de outros veículos nos acidentes',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=8)

# -------------------------------------------------------------
# Tipos de sinistro

top_tipo_sinistro = main_df['Tipo de Sinistro'].value_counts().nlargest(5).index
top_5_df = main_df[main_df['Tipo de Sinistro'].isin(top_tipo_sinistro)]


sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(15, 5))
sns.countplot(data=top_5_df, x='Tipo de Sinistro', order=top_tipo_sinistro, color='black')

plt.title('Tipos de sinístros',fontsize=19)
plt.ylabel('N° de vítimas',fontsize=15)
plt.xlabel(' ')
plt.xticks(fontsize=9)



'''Conclusão dos dados
Alguns dados relevantes:

Os homens representaram 81.6% das mortes;

Os condutores corresponderam a 57.73% das mortes;

Os condutores e passageiros costumam ser jovens, enquanto os pedestres costumam ser mais velhos;

As vias municipais tiveram mais mortes que as rodovias

O mês de março obteve o maior número de mortos;

80% dos acidentes fatais resultaram em morte no mesmo dia;

O município com mais mortes é a capital, com cerca de 4663 mortes nesse período de 5 anos, correspondendo a 17,5%;

Ocorreramm mais mortes diárias nos finais de semana do que dos dias de semana (19,78% das mortes totais no sábado e 19,43% no domingo);

A noite se mostrou muito mais perigosa que os outros turnos do dia (35,5% das mortes ocorreram na noite);

Aproximadamente 81% dos acidentes tinham outro veículo envolvido. E quando tinham, 43,5% possuíam envolvimento de automóvel;

O tipo mais comum desses acidentes (45,4%) foi colisão, o segundo foi atropelamento(34,8%)

22.18% foram acidentes frontais, enquanto 21,47% ocorreram em cruzamento de vias.'''

plt.show()