import subprocess
import sys

# Lista de pacotes que você deseja instalar
pacotes = ["reportlab", "selenium", "mysql","requests"]  # Adicione ou remova pacotes conforme necessário

# Executando o comando pip install para cada pacote
for pacote in pacotes:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pacote])
