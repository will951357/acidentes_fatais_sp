import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import cinza_escuro, cores_genero, paleta_tons_escuros

def analyze_age_distribution(main_df):
    # Filtrar e converter as idades
    main_df['Idade da vítima'] = main_df['Idade da vítima'].dropna().astype(int)

    # Separar por gênero e calcular estatísticas
    idade_homem = main_df[main_df['Sexo'] == 'MASCULINO']['Idade da vítima']
    idade_mulher = main_df[main_df['Sexo'] == 'FEMININO']['Idade da vítima']
    idades_combinadas = pd.concat([idade_homem, idade_mulher])
    idade_mais_obitos_homem = idade_homem.value_counts().idxmax()
    numero_de_obitos_homem = idade_homem.value_counts().max()
    
    idade_mais_obitos_mulher = idade_mulher.value_counts().idxmax()
    numero_de_obitos_mulher = idade_mulher.value_counts().max()
    
    media_idade_homem = idade_homem.mean()
    media_idade_mulher = idade_mulher.mean()

    plt.figure(figsize=(14, 7))
    sns.set_style('whitegrid')

    sns.histplot(idade_homem, color=cores_genero['MASCULINO'], label='Homens', binwidth=1)
    sns.histplot(idade_mulher, color=cores_genero['FEMININO'], label='Mulheres', binwidth=1)

    plt.xlabel('')
    plt.ylabel('Número de vítimas', fontsize=15, color=cinza_escuro)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=15)
    plt.title('Distribuição das idades por gênero', fontsize=20, color=cinza_escuro)
    plt.legend(title='Sexo')
    plt.ylim(0, max(numero_de_obitos_homem, numero_de_obitos_mulher) + 200)
    plt.grid(axis='both', color='lightgrey', linestyle='--')
    
    plt.annotate(
        f'Idade {idade_mais_obitos_homem}\n{numero_de_obitos_homem} Vítimas',
        xy=(idade_mais_obitos_homem, numero_de_obitos_homem),
        xytext=(idade_mais_obitos_homem, numero_de_obitos_homem),
        arrowprops=None,
        fontsize=12,
        color=cinza_escuro
    )
    
    plt.text(
        55, max(numero_de_obitos_homem, numero_de_obitos_mulher), 
        f'Média idade (Homens): {media_idade_homem:.0f} anos',
        fontsize=12, color=cores_genero['MASCULINO']
    )
    plt.text(
        55, max(numero_de_obitos_homem, numero_de_obitos_mulher) - 50, 
        f'Média idade (Mulheres): {media_idade_mulher:.0f} anos',
        fontsize=12, color=cores_genero['FEMININO']
    )

    plt.savefig('.\\media\\obitos_por_idade.png', bbox_inches='tight')
    plt.show()