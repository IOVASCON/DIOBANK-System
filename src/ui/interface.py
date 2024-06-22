import tkinter as tk
from tkinter import messagebox, ttk
import re  # Importação da biblioteca de expressões regulares, útil para validações de padrões de texto
from src.database import SessionLocal, init_db, clear_db  # Importações do módulo database para gerenciar a sessão, inicializar e limpar o banco de dados
from src.models.cliente import Cliente  # Importação do modelo Cliente
from src.models.conta import Conta  # Importação do modelo Conta
from src.models.historico import Historico  # Importação do modelo Historico
from random import randint  # Função para gerar números aleatórios, usada para criar números de conta
from datetime import datetime  # Importação para trabalhar com datas e horas

# A classe App define a interface gráfica do sistema bancário.
class App:
    def __init__(self, root):
        self.root = root  # Janela principal da aplicação
        self.root.title("DIOBANK - Seu banco de produtos tecnológicos")  # Título da janela
        self.root.geometry("800x600")  # Define o tamanho da janela
        self.create_widgets()  # Chama o método para criar os widgets da interface
        init_db()  # Inicializa o banco de dados

    def create_widgets(self):
        # Criação do menu à esquerda
        menu_frame = tk.Frame(self.root, bg="lightgrey", width=200, height=600)
        menu_frame.pack(side="left", fill="y")

        # Definição dos botões do menu e suas funções associadas
        botoes = [
            ("Cadastrar Cliente", self.cadastrar_cliente),
            ("Alterar Cliente", self.alterar_cliente),
            ("Excluir Cliente", self.excluir_cliente),
            ("Cadastrar Conta", self.cadastrar_conta),
            ("Visualizar Clientes", self.visualizar_clientes),
            ("Visualizar Contas", self.visualizar_contas),
            ("PRODUTOS", self.mostrar_produtos),  # Novo menu de produtos
            ("Limpar Base de Dados", self.limpar_base_dados),
            ("Sair", self.root.quit)
        ]

        # Criação dos botões no menu
        for idx, (text, command) in enumerate(botoes):
            button = tk.Button(menu_frame, text=text, command=command, width=20, height=2)
            button.grid(row=idx, column=0, padx=10, pady=5)

        # Frame principal onde as operações são exibidas
        self.main_frame = tk.Frame(self.root, bg="white", width=600, height=600)
        self.main_frame.pack(side="right", fill="both", expand=True)

    def limpar_base_dados(self):
        # Função para limpar a base de dados
        resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja limpar a base de dados?")
        if resposta:
            clear_db()
            messagebox.showinfo("Sucesso", "Base de dados limpa com sucesso.")
            self.clear_main_frame()

    def mostrar_produtos(self):
        # Função para exibir os produtos no frame principal
        self.clear_main_frame()
        tk.Label(self.main_frame, text="PRODUTOS").grid(row=0, column=1)

        produtos_frame = tk.Frame(self.main_frame, bg="white")
        produtos_frame.grid(row=1, column=0, columnspan=2)

        botoes_produtos = [
            ("Cursos", self.cursos),
            ("Bootcamp", self.bootcamp),
            ("Mentorias", self.mentorias),
            ("Desafios", self.desafios)
        ]

        # Criação dos botões de produtos
        for idx, (text, command) in enumerate(botoes_produtos):
            button = tk.Button(produtos_frame, text=text, command=command, width=20, height=2)
            button.grid(row=idx, column=0, padx=10, pady=5)

    def cursos(self):
        # Função para exibir a tela de cursos
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Cursos").grid(row=0, column=1)
        # Adicione lógica para a tela de cursos aqui

    def bootcamp(self):
        # Função para exibir a tela de bootcamp
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Bootcamp").grid(row=0, column=1)
        # Adicione lógica para a tela de bootcamp aqui

    def mentorias(self):
        # Função para exibir a tela de mentorias
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Mentorias").grid(row=0, column=1)
        # Adicione lógica para a tela de mentorias aqui

    def desafios(self):
        # Função para exibir a tela de desafios
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Desafios").grid(row=0, column=1)
        # Adicione lógica para a tela de desafios aqui

    def cadastrar_cliente(self):
        # Função para exibir a tela de cadastro de cliente
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Cadastrar Cliente").grid(row=0, column=1)

        tk.Label(self.main_frame, text="Nome:").grid(row=1, column=0)
        entry_nome = tk.Entry(self.main_frame)
        entry_nome.grid(row=1, column=1)

        tk.Label(self.main_frame, text="CPF:").grid(row=2, column=0)
        entry_cpf = tk.Entry(self.main_frame)
        entry_cpf.grid(row=2, column=1)
        entry_cpf.bind('<KeyRelease>', lambda event: self.formatar_cpf(event, entry_cpf))

        tk.Label(self.main_frame, text="Endereço:").grid(row=3, column=0)
        entry_endereco = tk.Entry(self.main_frame)
        entry_endereco.grid(row=3, column=1)

        tk.Label(self.main_frame, text="Tipo:").grid(row=4, column=0)
        combobox_tipo = ttk.Combobox(self.main_frame, values=["Pessoa Física", "Pessoa Jurídica"])
        combobox_tipo.grid(row=4, column=1)

        def submit():
            # Função para submeter o cadastro do cliente
            nome = entry_nome.get()
            cpf = entry_cpf.get()
            endereco = entry_endereco.get()
            tipo = combobox_tipo.get()
            if nome and cpf and endereco and tipo:  # Corrigido o erro de sintaxe aqui
                db = SessionLocal()
                cliente = Cliente(nome=nome, cpf=cpf, endereco=endereco, tipo=tipo)
                db.add(cliente)
                db.commit()
                db.close()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                self.clear_main_frame()
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")

        tk.Button(self.main_frame, text="Cadastrar", command=submit).grid(row=5, column=1)

    def alterar_cliente(self):
        # Função para exibir a tela de alteração de cliente
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Alterar Cliente").grid(row=0, column=1)

        tk.Label(self.main_frame, text="CPF do Cliente:").grid(row=1, column=0)
        entry_cpf = tk.Entry(self.main_frame)
        entry_cpf.grid(row=1, column=1)
        entry_cpf.bind('<KeyRelease>', lambda event: self.formatar_cpf(event, entry_cpf))

        def buscar_cliente():
            # Função para buscar um cliente pelo CPF
            cpf = self.formatar_cpf_completo(entry_cpf.get())
            db = SessionLocal()
            cliente = db.query(Cliente).filter_by(cpf=cpf).first()
            if cliente:
                db.close()
                self.mostrar_dados_cliente(cliente)
            else:
                db.close()
                messagebox.showwarning("Aviso", "Cliente não encontrado!")

        tk.Button(self.main_frame, text="Buscar", command=buscar_cliente).grid(row=1, column=2)

    def mostrar_dados_cliente(self, cliente):
        # Função para exibir os dados do cliente a serem alterados
        tk.Label(self.main_frame, text="Nome:").grid(row=2, column=0)
        entry_nome = tk.Entry(self.main_frame)
        entry_nome.grid(row=2, column=1)
        entry_nome.insert(0, cliente.nome)

        tk.Label(self.main_frame, text="Endereço:").grid(row=3, column=0)
        entry_endereco = tk.Entry(self.main_frame)
        entry_endereco.grid(row=3, column=1)
        entry_endereco.insert(0, cliente.endereco)

        tk.Label(self.main_frame, text="Tipo:").grid(row=4, column=0)
        combobox_tipo = ttk.Combobox(self.main_frame, values=["Pessoa Física", "Pessoa Jurídica"])
        combobox_tipo.grid(row=4, column=1)
        combobox_tipo.set(cliente.tipo)

        def submit_alteracao():
            # Função para submeter as alterações do cliente
            nome = entry_nome.get()
            endereco = entry_endereco.get()
            tipo = combobox_tipo.get()
            if nome and endereco and tipo:  # Corrigido o erro de sintaxe aqui
                db = SessionLocal()
                cliente_atualizar = db.query(Cliente).filter_by(id=cliente.id).first()
                cliente_atualizar.nome = nome
                cliente_atualizar.endereco = endereco
                cliente_atualizar.tipo = tipo
                db.commit()
                db.close()
                messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")
                self.clear_main_frame()
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")

        tk.Button(self.main_frame, text="Salvar Alterações", command=submit_alteracao).grid(row=5, column=1)

    def excluir_cliente(self):
        # Função para exibir a tela de exclusão de cliente
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Excluir Cliente").grid(row=0, column=1)

        tk.Label(self.main_frame, text="CPF do Cliente:").grid(row=1, column=0)
        entry_cpf = tk.Entry(self.main_frame)
        entry_cpf.grid(row=1, column=1)
        entry_cpf.bind('<KeyRelease>', lambda event: self.formatar_cpf(event, entry_cpf))

        def buscar_cliente_para_excluir():
            # Função para buscar e excluir um cliente pelo CPF
            cpf = self.formatar_cpf_completo(entry_cpf.get())
            db = SessionLocal()
            cliente = db.query(Cliente).filter_by(cpf=cpf).first()
            if cliente:
                db.delete(cliente)
                db.commit()
                db.close()
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.clear_main_frame()
            else:
                db.close()
                messagebox.showwarning("Aviso", "Cliente não encontrado!")

        tk.Button(self.main_frame, text="Excluir", command=buscar_cliente_para_excluir).grid(row=1, column=2)

    def cadastrar_conta(self):
        # Função para exibir a tela de cadastro de conta
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Cadastrar Conta").grid(row=0, column=1)

        tk.Label(self.main_frame, text="Tipo:").grid(row=1, column=0)
        combobox_tipo = ttk.Combobox(self.main_frame, values=["Pessoa Física", "Pessoa Jurídica"])
        combobox_tipo.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Agência:").grid(row=2, column=0)
        entry_agencia = tk.Entry(self.main_frame)
        entry_agencia.grid(row=2, column=1)

        tk.Label(self.main_frame, text="CPF do Cliente:").grid(row=3, column=0)
        entry_cpf_cliente = tk.Entry(self.main_frame)
        entry_cpf_cliente.grid(row=3, column=1)
        entry_cpf_cliente.bind('<KeyRelease>', lambda event: self.formatar_cpf(event, entry_cpf_cliente))

        tk.Label(self.main_frame, text="Saldo:").grid(row=4, column=0)
        entry_saldo = tk.Entry(self.main_frame)
        entry_saldo.grid(row=4, column=1)
        entry_saldo.bind('<KeyRelease>', lambda event: self.formatar_saldo(event, entry_saldo))

        def submit():
            # Função para submeter o cadastro da conta
            tipo = combobox_tipo.get()
            agencia = entry_agencia.get()
            cpf_cliente = entry_cpf_cliente.get()
            saldo = entry_saldo.get().replace("R$ ", "").replace(".", "").replace(",", ".")
            if tipo and agencia and cpf_cliente and saldo:  # Corrigido o erro de sintaxe aqui
                db = SessionLocal()
                cpf_cliente_formatado = self.formatar_cpf_completo(cpf_cliente)
                cliente = db.query(Cliente).filter_by(cpf=cpf_cliente_formatado).first()
                if cliente:
                    num_conta = str(randint(1000, 9999))
                    conta = Conta(tipo=tipo, agencia=agencia, num=num_conta, id_cliente=cliente.id, saldo=saldo)
                    db.add(conta)
                    historico = Historico(historico="Abertura de conta", saldo=saldo, conta=conta)
                    db.add(historico)
                    db.commit()
                    db.close()
                    messagebox.showinfo("Sucesso", f"Conta cadastrada com sucesso! Número da conta: {num_conta}")
                    self.clear_main_frame()
                else:
                    db.close()
                    messagebox.showwarning("Aviso", "Cliente não encontrado!")
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")

        tk.Button(self.main_frame, text="Cadastrar", command=submit).grid(row=5, column=1)

    def visualizar_clientes(self):
        # Função para exibir a lista de clientes
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Clientes").grid(row=0, column=0, sticky="w")
        db = SessionLocal()
        clientes = db.query(Cliente).all()
        db.close()
        for idx, cliente in enumerate(clientes):
            tk.Label(self.main_frame, text=f"{cliente.id} - {cliente.nome}, CPF: {cliente.cpf}, Endereço: {cliente.endereco}, Tipo: {cliente.tipo}", anchor="w").grid(row=idx + 1, column=0, sticky="w")

    def visualizar_contas(self):
        # Função para exibir a lista de contas
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Contas").grid(row=0, column=0, sticky="w")
        db = SessionLocal()
        contas = db.query(Conta).all()
        db.close()
        for idx, conta in enumerate(contas):
            saldo_formatado = f"R$ {float(conta.saldo):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tk.Label(self.main_frame, text=f"{conta.id} - Tipo: {conta.tipo}, Agência: {conta.agencia}, Número: {conta.num}, ID Cliente: {conta.id_cliente}, Saldo: {saldo_formatado}", anchor="w").grid(row=idx + 1, column=0, sticky="w")

    def formatar_cpf(self, event, entry):
        # Função para formatar o CPF à medida que é digitado
        text = entry.get().replace(".", "").replace("-", "")
        new_text = ""
        for i in range(len(text)):
            if i in [2, 5]:
                new_text += text[i] + "."
            elif i == 8:
                new_text += text[i] + "-"
            else:
                new_text += text[i]
        entry.delete(0, tk.END)
        entry.insert(0, new_text)

    def formatar_cpf_completo(self, cpf):
        # Função para formatar completamente o CPF
        cpf = cpf.replace(".", "").replace("-", "")
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def formatar_saldo(self, event, entry):
        # Função para formatar o saldo no formato brasileiro
        text = entry.get().replace("R$ ", "").replace(".", "").replace(",", "")
        if text.isdigit():
            if len(text) > 2:
                text = f"R$ {int(text[:-2]):,}.{text[-2:]}".replace(",", ".")
            else:
                text = f"R$ 0,{text.zfill(2)}"
            entry.delete(0, tk.END)
            entry.insert(0, text)

    def clear_main_frame(self):
        # Função para limpar o frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Código principal para iniciar a aplicação
    root = tk.Tk()
    app = App(root)
    root.mainloop()
