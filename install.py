import sys
from cx_Freeze import setup, Executable

# Definir informações do executável
exe = Executable(
    script="main.py",  # O nome do arquivo de script principal
    base="Win32GUI" if sys.platform == "win32" else None,  # Usar interface gráfica no Windows
    icon="icon.ico"  # Caminho para o ícone (se necessário)
)

# Definir informações do pacote
options = {
    "build_exe": {
        "packages": ["os"],  # Pacotes a serem incluídos
        # Outros arquivos que você deseja incluir, como imagens, etc.
    },
}

# Criar o executável
setup(
    name="MeuPrograma",  # Nome do programa
    version="1.0",  # Versão do programa
    description="Descrição do programa",
    options=options,
    executables=[exe]
)
