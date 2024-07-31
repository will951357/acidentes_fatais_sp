# __init__.py

from .data_processing import load_and_clean_data
from .gender_analysis import analyze_gender_distribution
from .age_analysis import analyze_age_distribution
from .victim_type_analysis import analyze_victim_types, analyze_victim_types_gender
from .who_analysis import (analyze_age_distribution_by_victim_type, analyze_means_of_transport,
                            analyze_means_of_transport_gender)
from .geographical_analysis import (analyze_geographical_distribution, analyze_road_types, 
                                    analyze_road_type_by_gender, analyze_road_type_by_victim, 
                                    analyze_road_type_by_vehicle)
from .temporal_analysis import (analyze_monthly_frequency, analyze_weekday_distribution, 
                                analyze_shift_distribution, analyze_time_to_death)
from .how_analysis import analyze_other_vehicle_involvement, analyze_accident_types
from .formatar_plots import format_plot, add_labels
