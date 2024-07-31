import pandas as pd
from pathlib import Path

def load_and_clean_data(file_path):
    # Carregar os dados
    main_df = pd.read_csv(file_path, encoding='latin1', delimiter=';')

    # Remover dados com status 'NAO DISPONIVEL'
    main_df = main_df[main_df['Sexo'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Meio de locomoção da vítima'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Tipo de vítima'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Tipo de Sinistro'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Tipo de via'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Turno'] != 'NAO DISPONIVEL']
    main_df = main_df[main_df['Outro Veículo Envolvido'] != 'NAO DISPONIVEL']
    return main_df