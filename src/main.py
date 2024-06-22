import sys
import os

# Adiciona o diretório raiz ao caminho de pesquisa de módulos
# Isso permite que módulos sejam importados mesmo que estejam em diretórios diferentes.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ui.interface import App  # Importa a classe App do módulo interface para criar a interface gráfica
from src.database import init_db, update_db  # Importa as funções init_db e update_db para gerenciar o banco de dados
import tkinter as tk  # Importa o tkinter para criar a interface gráfica

def main():
    # Atualiza o banco de dados para garantir que a coluna 'tipo' exista
    update_db()
    # Inicializa o banco de dados e cria as tabelas
    init_db()
    # Inicializa a interface gráfica
    root = tk.Tk()  # Cria a janela principal da aplicação
    app = App(root)  # Cria uma instância da classe App, passando a janela principal
    root.mainloop()  # Inicia o loop principal do tkinter, que mantém a janela aberta e responsiva

if __name__ == "__main__":
    main()  # Chama a função main se este arquivo for executado como script principal
