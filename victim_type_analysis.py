import matplotlib.pyplot as plt
import seaborn as sns
from config import cores_genero, cinza_escuro, paleta_tipo_vitima
from formatar_plots import format_plot, add_labels

def analyze_victim_types(main_df):
    vitimas = main_df['Tipo de vítima'].value_counts()
    vitimas_perc = (vitimas / vitimas.sum()) * 100
    max_value = max(vitimas.values)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=vitimas.index, y=vitimas.values,order=vitimas.index, palette=paleta_tipo_vitima, ax=ax)
    plt.title('Classificação das Vítimas por Tipo', fontsize=20, color=cinza_escuro, pad=20)
    format_plot(ax, max_value)
    add_labels(ax, vitimas.values, max_value, vitimas_perc)
    plt.legend(title='Gênero')
    plt.savefig('.\\media\\vitimas_tipo.png', bbox_inches='tight')
    plt.show()
    

def analyze_victim_types_gender(main_df):

    vitimas = main_df['Tipo de vítima'].value_counts()
    vitimas_perc = (vitimas / vitimas.sum()) * 100
    max_value = max(vitimas.values)

    # Gráfico de barras dividido por gênero
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Tipo de vítima', hue='Sexo', palette=cores_genero, ax=ax, order=vitimas.index)
    format_plot(ax, max_value)
    add_labels(ax, vitimas.values, max_value, vitimas_perc)
    plt.title('Classificação das Vítimas por Tipo e Gênero', fontsize=20, color=cinza_escuro, pad=20)
    plt.legend(title='Gênero')
    plt.savefig('.\\media\\vitimas_tipo_genero_.png', bbox_inches='tight')
    plt.show()
