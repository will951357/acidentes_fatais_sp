import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import cores_hora, cinza_escuro, paleta_tons_escuros
from formatar_plots import format_plot, add_labels

def analyze_monthly_frequency(main_df):

    mes = main_df['Mês do Óbito'].value_counts()
    mes_perc = (mes / mes.sum()) * 100
    max_value = max(mes.values)

    mes_obito = main_df['Mês do Óbito'].value_counts().sort_index()
    df_area = pd.DataFrame({'Mês do Óbito': mes_obito.index, 'Número de Vítimas': mes_obito.values})

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('whitegrid')
    plt.xticks(df_area['Mês do Óbito'], ha='right')
    sns.lineplot(x='Mês do Óbito', y='Número de Vítimas', data=df_area, color=cinza_escuro, marker='o', linewidth=2.4, linestyle='-')
    plt.title('Frequência de acidentes fatais distribuidos por mês', fontsize=15, color=cinza_escuro)
    plt.ylabel('Número de vítimas', fontsize=13, color=cinza_escuro)
    plt.xlabel('')
    plt.xticks(fontsize=13)
    plt.savefig('.\\media\\vitimas_por_mes.png', bbox_inches='tight')
    plt.show()

def analyze_weekday_distribution(main_df):
    dia_semana_obito = main_df['Dia da Semana'].value_counts().sort_index()
    dia_semana_obito_perc = (dia_semana_obito / dia_semana_obito.sum()) * 100
    max_value = max(dia_semana_obito.values)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('whitegrid')
    sns.countplot(data=main_df, x='Dia da Semana', palette=paleta_tons_escuros, order=dia_semana_obito.index)
    format_plot(ax, max_value)
    add_labels(ax, dia_semana_obito.values, max_value, dia_semana_obito_perc.values)
    plt.title('Acidentes fatais de acordo com os dias da semana', fontsize=15, color=cinza_escuro)
    plt.savefig('.\\media\\vitimas_dia_semana.png', bbox_inches='tight')
    plt.show()

def analyze_shift_distribution(main_df):
    turno_obito = main_df['Turno'].value_counts().sort_index()
    turno_obito_perc = (turno_obito / turno_obito.sum()) * 100
    max_value = max(turno_obito.values)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('whitegrid')  
    sns.countplot(data=main_df, x='Turno', palette=paleta_tons_escuros, order=turno_obito.index)
    format_plot(ax, max_value)
    add_labels(ax, turno_obito.values, max_value, turno_obito_perc.values)
    plt.title('Mortes fatais de acordo com os turnos do dia', fontsize=15, color=cinza_escuro)
    plt.savefig('.\\media\\vitimas_por_turno.png', bbox_inches='tight')
    plt.show()

def analyze_time_to_death(main_df):
    tempo_acidente_obito = main_df['Tempo entre o Sinistro e o Óbito'].value_counts()
    tempo_acidente_obito_perc = (tempo_acidente_obito / tempo_acidente_obito.sum()) * 100

    print(tempo_acidente_obito_perc)

