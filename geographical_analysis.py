import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as ctx
from config import paleta_tipo_veiculo, paleta_genero, cinza_escuro
from formatar_plots import format_plot, add_labels

def analyze_geographical_distribution(main_df):
    # Converter as colunas para float
    main_df['latitude'] = main_df['latitude'].str.replace(',', '.').astype(float)
    main_df['longitude'] = main_df['longitude'].str.replace(',', '.').astype(float)

    # Remover valores ausentes
    main_df_filtered = main_df.dropna(subset=['latitude', 'longitude'])

    # Filtrar coordenadas dentro da faixa esperada para São Paulo
    main_df_filtered = main_df_filtered[
        (main_df_filtered['latitude'] >= -25.4383) & (main_df_filtered['latitude'] <= -19.7518) &
        (main_df_filtered['longitude'] >= -53.0288) & (main_df_filtered['longitude'] <= -44.0723)
    ]

    # Criar um GeoDataFrame
    gdf = gpd.GeoDataFrame(main_df_filtered, geometry=gpd.points_from_xy(main_df_filtered.longitude, main_df_filtered.latitude))

    # Definir o CRS para WGS 84 e reprojetar para Web Mercator
    gdf.crs = {'init': 'epsg:4326'}
    gdf = gdf.to_crs(epsg=3857)

    # Criar o gráfico de distribuição geográfica
    fig, ax = plt.subplots(figsize=(20, 12))
    gdf.plot(ax=ax, markersize=1, color='black', alpha=0.5)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.title('Concentração de acidentes fatais no Estado de São Paulo (2015 - 2024)', fontsize=15, color=cinza_escuro)
    ax.set_axis_off()
    plt.savefig('.\\media\\densidade_geografica.png', bbox_inches='tight')
    plt.show()

    # Contagem e percentual de mortes por município
    mortes_por_municipio = main_df['Município'].value_counts()
    mortes_por_municipio_perc = (mortes_por_municipio / mortes_por_municipio.sum()) * 100
    print(mortes_por_municipio)
    print(mortes_por_municipio_perc)

def analyze_road_types(main_df):
    vias = main_df['Tipo de via'].value_counts()
    vias_perc = (vias / vias.sum()) * 100
    max_value = max(vias.values)

    # Gráfico de tipos de via
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Tipo de via', palette=paleta_tipo_veiculo, order=vias.index)
    plt.title('Tipos de via', fontsize=15, color=cinza_escuro)
    
    format_plot(ax, max_value)
    add_labels(ax, vias.values, max_value, vias_perc)
    plt.savefig('.\\media\\tipos_vias.png', bbox_inches='tight')
    plt.show()

def analyze_road_type_by_gender(main_df):
    # Mortes em vias municipais x Rodovias por Gênero
    vias = main_df['Tipo de via'].value_counts()
    vias_perc = (vias / vias.sum()) * 100
    max_value = max(vias.values)

    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Tipo de via', hue='Sexo', palette=paleta_genero, order=vias.index)
    plt.title('Número de vítimas em Vias Municipais X Rodovias (Gênero)', fontsize=15, color=cinza_escuro)
    format_plot(ax, max_value + 5000)
    add_labels(ax, vias.values, max_value, vias_perc)
    plt.legend(title='Gênero', loc='upper right')

    plt.savefig('.\\media\\tipos_vias_genero.png', bbox_inches='tight')
    plt.show()

def analyze_road_type_by_victim(main_df):
    # Mortes em vias municipais x Rodovias por Tipo de Vítima
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Tipo de via', hue='Tipo de vítima', palette=paleta_tipo_veiculo)
    plt.title('Número de vítimas em Vias Municipais X Rodovias (tipo de vítima)', fontsize=15, color=cinza_escuro, pad=20)
    plt.ylabel('Número de vítimas', fontsize=15)
    plt.xlabel(' ')
    plt.xticks(fontsize=13, color=cinza_escuro)
    plt.legend(title='Tipo de vítima', loc='upper right')
    plt.savefig('.\\media\\tipos_vias_vitimas.png', bbox_inches='tight')
    plt.show()

def analyze_road_type_by_vehicle(main_df):
    # Mortes em vias municipais x Rodovias por Tipo de Veículo
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Tipo de via', hue='Meio de locomoção da vítima', palette=paleta_tipo_veiculo)
    plt.title('Número de vítimas em Vias Municipais X Rodovias (Tipo de Veículo)', fontsize=15, color=cinza_escuro)
    plt.ylabel('Número de vítimas', fontsize=13, color=cinza_escuro)
    plt.xlabel(' ')
    plt.xticks(fontsize=13)
    plt.legend(title='Veículo da vítima', loc='upper right')
    plt.savefig('.\\media\\via_por_veiculo.png', bbox_inches='tight')
    plt.show()