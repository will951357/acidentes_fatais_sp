# analysis.py

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
    print(f"Import error: {e}")
