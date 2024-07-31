
import sys
import os

# Obtém o diretório onde o script está localizado
current_dir = os.path.dirname(os.path.abspath(__file__))
# Define o diretório principal, que está um nível acima do diretório atual
main_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Adiciona o diretório principal ao sys.path
sys.path.insert(0, main_dir)

print("Current working directory:", main_dir)
print("Python path:", sys.path)

try:
    import acidentes_fatais
    print("Imports successful!")
except ModuleNotFoundError as e:
    raise e

# Adiciona o caminho do diretório pai ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from acidentes_fatais import load_and_clean_data, analyze_gender_distribution
from pathlib import Path

if __name__ == '__main__':
    root_path = Path(__file__).parent
    file_path = root_path / 'obitos.csv'
    main_df = acidentes_fatais.load_and_clean_data(file_path)
    # acidentes_fatais.analyze_gender_distribution(main_df)
    # acidentes_fatais.analyze_age_distribution(main_df)
    # acidentes_fatais.analyze_victim_types(main_df)
    # acidentes_fatais.analyze_victim_types_gender(main_df)
    # acidentes_fatais.analyze_age_distribution_by_victim_type(main_df)
    # acidentes_fatais.analyze_means_of_transport(main_df)
    # acidentes_fatais.analyze_means_of_transport_gender(main_df)
    # acidentes_fatais.analyze_geographical_distribution(main_df)
    # acidentes_fatais.analyze_road_types(main_df)
    # acidentes_fatais.analyze_road_type_by_gender(main_df)
    # acidentes_fatais.analyze_road_type_by_victim(main_df)
    # acidentes_fatais.analyze_road_type_by_vehicle(main_df)
    # acidentes_fatais.analyze_monthly_frequency(main_df)
    # acidentes_fatais.analyze_weekday_distribution(main_df)
    # acidentes_fatais.analyze_shift_distribution(main_df)
    # acidentes_fatais.analyze_time_to_death(main_df)
    # acidentes_fatais.analyze_other_vehicle_involvement(main_df)
    acidentes_fatais.analyze_accident_types(main_df)
