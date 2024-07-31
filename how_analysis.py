import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import cores_hora, cinza_escuro, paleta_tons_escuros
from formatar_plots import format_plot, add_labels

def analyze_other_vehicle_involvement(main_df):
    outro_veiculo_envolvido = main_df['Outro Veículo Envolvido'].value_counts()
    outro_veiculo_envolvido_perc = (outro_veiculo_envolvido / outro_veiculo_envolvido.sum()) * 100
    max_value = max(outro_veiculo_envolvido)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('whitegrid')
    sns.countplot(data=main_df, x='Outro Veículo Envolvido',
                   order=outro_veiculo_envolvido.index, palette=paleta_tons_escuros)
    format_plot(ax, max_value)
    add_labels(ax, outro_veiculo_envolvido.values, max_value, outro_veiculo_envolvido_perc.values)
    plt.title('Envolvimento de outros veículos nos acidentes', fontsize=15, color=cinza_escuro)
    plt.savefig('.\\media\\veiculos_envolvidos.png', bbox_inches='tight')
    plt.show()

def analyze_accident_types(main_df):
    
    tipo_sinistro = main_df['Tipo de Sinistro'].value_counts()
    tipo_sinistro_perc = (tipo_sinistro / tipo_sinistro.sum()) * 100
    
    print(tipo_sinistro.index)

    top_tipo_sinistro = tipo_sinistro.nlargest(5).index
    top_5_df = main_df[main_df['Tipo de Sinistro'].isin(top_tipo_sinistro)]

    ttipo_sinistro = top_5_df['Tipo de Sinistro'].value_counts()
    ttipo_sinistro_perc = (ttipo_sinistro / ttipo_sinistro.sum()) * 100
    max_value = max(ttipo_sinistro)
    print(ttipo_sinistro)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('whitegrid')
    sns.countplot(data=top_5_df, x='Tipo de Sinistro', order=ttipo_sinistro.index, palette=paleta_tons_escuros)
    add_labels(ax, ttipo_sinistro.values, max_value, ttipo_sinistro_perc.values)
    format_plot(ax, max_value)
    plt.title('Tipos de acidentes fatais (Top 5)', fontsize=15, color=cinza_escuro)
    plt.savefig('.\\media\\tipos_acidentes.png', bbox_inches='tight')
    plt.show()
