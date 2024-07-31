import matplotlib.pyplot as plt
import seaborn as sns
from config import cores_genero, cinza_escuro, paleta_tipo_veiculo
from formatar_plots import add_labels, format_plot

def analyze_age_distribution_by_victim_type(main_df):
    # Distribuição de idade das diferentes vítimas
    fig, ax = plt.subplots(figsize=(15, 9))
    sns.violinplot(x='Tipo de vítima', y='Idade da vítima', hue='Sexo', palette=cores_genero, data=main_df)
    plt.xlim(-0.5, 2.5)
    plt.title('Distribuição etária das vítimas por Tipo e Gênero', fontsize=15, color=cinza_escuro)
    plt.xlabel(' ')
    plt.ylabel('Faixa etária', fontsize=13, color=cinza_escuro)
    plt.legend(title='Genêro')
    plt.savefig('.\\media\\distribuicao_idade_vitima_.png', bbox_inches='tight')
    plt.show()

def analyze_means_of_transport(main_df):
    # Gráfico de contagem por meio de locomoção

    veiculos = main_df['Meio de locomoção da vítima'].value_counts()
    veiculos_perc = (veiculos / veiculos.sum()) * 100
    max_value = max(veiculos.values)

    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.countplot(data=main_df, x='Meio de locomoção da vítima', order=veiculos.index, palette=paleta_tipo_veiculo)
    format_plot(ax, max_value)
    plt.xlabel(' ')
    add_labels(ax, veiculos.values, max_value, veiculos_perc)
    plt.title('Veículos das vítimas', fontsize=20, color=cinza_escuro, pad=20)
    plt.savefig('.\\media\\vitimas_por_veiculos.png', bbox_inches='tight')
    plt.show()


def analyze_means_of_transport_gender(main_df):
    # Gráfico de caixa por meio de locomoção
    veiculos = main_df['Meio de locomoção da vítima'].value_counts()
    veiculos_perc = (veiculos / veiculos.sum()) * 100
    max_value = max(veiculos.values)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.boxplot(x='Meio de locomoção da vítima',
                y='Idade da vítima', hue='Sexo',
                palette=cores_genero, order=veiculos.index,
                data=main_df
            )
    plt.title('Faixa etária das vítimas por veículo', fontsize=21)
    plt.xlabel(' ')
    plt.ylabel('Faixa etária', fontsize=13, color=cinza_escuro)
    plt.legend(title='Genêro')
    plt.savefig('.\\media\\idade_vitimas_veiculo.png', bbox_inches='tight')
    plt.show()

