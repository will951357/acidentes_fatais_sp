import matplotlib.pyplot as plt
import seaborn as sns
from config import cinza_escuro
from data_processing import load_and_clean_data
from pathlib import Path

def analyze_gender_distribution(main_df):

    def func(pct, allvalues):
        absolute = int(pct / 100. * sum(allvalues))
        return f'{absolute} ({pct:.2f}%)'

    # Análise e visualização por gênero
    cores=sns.color_palette(['#4682b4', '#d6a1a1'])

    genero = main_df['Sexo'].value_counts()
    genero_perc = (genero/genero.sum())*100

    print(genero_perc)

    fig, ax = plt.subplots(figsize=(7, 7))
    sns.set_style('ticks')
    
    ax.pie(genero_perc, labels=genero_perc.index, autopct=lambda pct: func(pct, genero), startangle=140, colors=cores)
    plt.title('Vítimas por gênero', fontsize=21, color=cinza_escuro)
    plt.show()