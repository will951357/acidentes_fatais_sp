import seaborn as sns

# Cores
cores_tons_escuros = ['#2E4A62', '#46637F', '#5D7D9B', '#4B4B4B', '#C0C0C0']
cores_hora = ['#FFD700', '#FFD700', '#8B0000', '#FFD700', '#C0C0C0']
cores_dia = ['#8B0000', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFA500', '#8B0000']
cores_genero = {'MASCULINO': '#4682b4', 'FEMININO': '#d6a1a1'}
cores_tipo_vitima = ["#2E4A62", "#5D7D9B", "#C0C0C0"]
cinza_escuro = '#4A4A4A'
cores_veiculos = ['#2E4A62', '#5D7D9B', '#C0C0C0', '#5E7F9A', '#6A8BAF', '#7A9ABF', '#8ABBD3',]

# Paletas
#paleta_tipo_veiculo = sns.color_palette("husl", 7)
paleta_tipo_veiculo = sns.color_palette(cores_veiculos)
paleta_degrade = sns.cubehelix_palette(8, start=2, rot=0, dark=0, light=.75, reverse=True)
paleta_hora = sns.color_palette(cores_hora)
paleta_tipo_vitima = sns.color_palette(cores_tipo_vitima)
paleta_genero = cores_genero
paleta_dia = sns.color_palette(cores_dia)
paleta_tons_escuros = sns.color_palette(cores_tons_escuros)