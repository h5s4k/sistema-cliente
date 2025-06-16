import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import sqlite3
import os
import sys
import re
import csv

class AppClientesSimplificado:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Clientes Simplificado")
        self.root.geometry("800x600")
        
        # Conexão com SQLite (arquivo local)
        if getattr(sys, 'frozen', False):
            # Se estiver rodando como executável
            application_path = os.path.dirname(sys.executable)
        else:
            # Se estiver rodando em desenvolvimento
            application_path = os.path.dirname(os.path.abspath(__file__))
    
        self.db_file = os.path.join(application_path, "clientes.db")
        self.conn = self.conectar_banco()
        self.criar_tabela()
        
        # Interface gráfica
        self.criar_widgets()
        
        # Carrega clientes existentes
        self.carregar_clientes()
    
    def conectar_banco(self):
        """Estabelece conexão com o banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as err:
            messagebox.showerror("Erro SQLite", f"Falha na conexão:\n{err}")
            return None
    
    def criar_tabela(self):
        """Cria a tabela clientes se não existir"""
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                email TEXT NOT NULL,
                                telefone TEXT NOT NULL)''')
                self.conn.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar tabela:\n{e}")

    def importar_csv(self):
        """Importa clientes de um arquivo CSV"""
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if not caminho_arquivo:
            return
        
        try:
            with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile)
                inseridos = 0
                for linha in leitor:
                    nome = linha["nome"].strip()
                    email = linha.get("email", "").strip()
                    telefone = linha["telefone"].strip()

                    if not nome or not telefone:
                        continue  # ignora entradas incompletas

                    # Verifica duplicidade
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM clientes WHERE telefone = ? OR (email = ? AND email != '')", 
                                 (telefone, email))
                    if cursor.fetchone():
                        continue  # já existe, ignora

                    # Insere no banco
                    cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                                (nome, email, telefone))
                    inseridos += 1

                self.conn.commit()
                self.carregar_clientes()
                messagebox.showinfo("Importação concluída", f"{inseridos} cliente(s) importado(s) com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar CSV:\n{e}")
    
    def criar_widgets(self):
        """Cria a interface gráfica"""
        # Frame de cadastro
        frame_cadastro = tk.LabelFrame(self.root, text="Cadastrar Cliente", padx=10, pady=10)
        frame_cadastro.pack(padx=10, pady=5, fill="x")
        
        # Campo Nome
        tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_cadastro, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        # Campo Email
        tk.Label(frame_cadastro, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_email = tk.Entry(frame_cadastro, width=40)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)
        
        # Campo Telefone
        tk.Label(frame_cadastro, text="Telefone:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_telefone = tk.Entry(frame_cadastro, width=40)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão Cadastrar
        btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar_cliente, width=15)
        btn_cadastrar.grid(row=3, column=1, pady=10, sticky="e")
        
        # Frame de listagem
        frame_lista = tk.LabelFrame(self.root, text="Clientes Cadastrados", padx=10, pady=10)
        frame_lista.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Treeview para exibir clientes com seleção múltipla
        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Nome", "Email", "Telefone"), 
                               show="headings", selectmode='extended')
        
        # Configuração das colunas
        colunas = [
            ("ID", 50),
            ("Nome", 200),
            ("Email", 200),
            ("Telefone", 100)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill="both", expand=True)
        
        # Frame de botões
        frame_botoes = tk.Frame(frame_lista)
        frame_botoes.pack(pady=5)

        # Botão Atualizar
        btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=self.carregar_clientes, width=15)
        btn_atualizar.pack(side="left", padx=5)
        
        # Botão Excluir Selecionados
        btn_excluir = tk.Button(frame_botoes, text="Excluir Selecionados", command=self.excluir_clientes_selecionados, width=15)
        btn_excluir.pack(side="left", padx=5)
        
        # Botão Editar (para edição única)
        btn_editar = tk.Button(frame_botoes, text="Editar", command=self.editar_cliente, width=15)
        btn_editar.pack(side="left", padx=5)

        # Botão Importar CSV
        btn_importar_csv = tk.Button(frame_botoes, text="Importar CSV", command=self.importar_csv, width=15)
        btn_importar_csv.pack(side="left", padx=5)
    
    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        
        # verifica o padrão de email:
        def email_valido(email):
            padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
            return re.match(padrao, email)
        
        if email and not email_valido(email):
            messagebox.showwarning("Aviso", "Email inválido!")
            return

        # Valida telefone, aceita apenas números com 10 ou 11 dígitos (sem letras ou símbolos)
        def telefone_valido(telefone):
            return telefone.isdigit() and len(telefone) in [10, 11]
        
        if not telefone_valido(telefone):
            messagebox.showwarning("Aviso", "Telefone inválido! Use apenas números (10 ou 11 dígitos).")
            return

        # Validação dos campos obrigatórios
        if not nome or not telefone:
            messagebox.showwarning("Aviso", "Nome e telefone são obrigatórios!")
            return
        
        try:
            if self.conn:
                cursor = self.conn.cursor()
    
                # Verifica duplicidade de telefone (obrigatório)
                cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
                if cursor.fetchone():
                    messagebox.showwarning("Aviso", "Telefone já cadastrado!")
                    return

                # Verifica duplicidade de email, se informado
                if email:
                    cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
                    if cursor.fetchone():
                        messagebox.showwarning("Aviso", "Email já cadastrado!")
                        return

                cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", 
                             (nome, email, telefone))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                self.limpar_campos()
                self.carregar_clientes()
        except sqlite3.Error as err:
            messagebox.showerror("Erro SQLite", f"Erro ao cadastrar:\n{err}")
    
    def carregar_clientes(self):
        """Carrega todos os clientes na treeview"""
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY nome")
                clientes = cursor.fetchall()
                
                # Limpa a treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Preenche com os dados
                for cliente in clientes:
                    self.tree.insert("", "end", values=cliente)
        except sqlite3.Error as err:
            messagebox.showerror("Erro SQLite", f"Falha ao carregar clientes:\n{err}")
    
    def excluir_clientes_selecionados(self):
        """Exclui todos os clientes selecionados na treeview"""
        selecionados = self.tree.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um ou mais clientes para excluir!")
            return
        
        # Obtém os IDs dos clientes selecionados
        ids_clientes = [self.tree.item(item)["values"][0] for item in selecionados]
        
        confirmacao = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir os {len(ids_clientes)} cliente(s) selecionado(s)?"
        )
        
        if confirmacao:
            try:
                if self.conn:
                    cursor = self.conn.cursor()
                    # Usamos uma única execução com parâmetros para todos os IDs
                    placeholders = ','.join(['?'] * len(ids_clientes))
                    cursor.execute(f"DELETE FROM clientes WHERE id IN ({placeholders})", ids_clientes)
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", f"{len(ids_clientes)} cliente(s) excluído(s) com sucesso!")
                    self.carregar_clientes()
            except sqlite3.Error as err:
                messagebox.showerror("Erro SQLite", f"Falha ao excluir clientes:\n{err}")
    
    def editar_cliente(self):
        """Edita o cliente selecionado - agora verifica seleção única"""
        selecionados = self.tree.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        if len(selecionados) > 1:
            messagebox.showwarning("Aviso", "Selecione apenas um cliente para editar!")
            return
        
        # Obtém os dados atuais
        item = self.tree.item(selecionados[0])
        id_cliente = item["values"][0]
        nome_atual = item["values"][1]
        email_atual = item["values"][2]
        telefone_atual = item["values"][3]
        
        # Janela de edição
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Cliente")
        janela_edicao.geometry("400x300")
        
        # Campos de edição
        tk.Label(janela_edicao, text="Nome:").pack(pady=(10,0))
        entry_nome_edit = tk.Entry(janela_edicao, width=40)
        entry_nome_edit.pack()
        entry_nome_edit.insert(0, nome_atual)
        
        tk.Label(janela_edicao, text="Email:").pack(pady=(10,0))
        entry_email_edit = tk.Entry(janela_edicao, width=40)
        entry_email_edit.pack()
        entry_email_edit.insert(0, email_atual)
        
        tk.Label(janela_edicao, text="Telefone:").pack(pady=(10,0))
        entry_telefone_edit = tk.Entry(janela_edicao, width=40)
        entry_telefone_edit.pack()
        entry_telefone_edit.insert(0, telefone_atual)
        
        def salvar_edicao():
            """Salva as alterações no banco de dados"""
            novo_nome = entry_nome_edit.get().strip()
            novo_email = entry_email_edit.get().strip()
            novo_telefone = entry_telefone_edit.get().strip()
            
            # Validações
            def email_valido(email):
                padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
                return re.match(padrao, email)
            
            if novo_email and not email_valido(novo_email):
                messagebox.showwarning("Aviso", "Email inválido!")
                return

            def telefone_valido(telefone):
                return telefone.isdigit() and len(telefone) in [10, 11]
            
            if not telefone_valido(novo_telefone):
                messagebox.showwarning("Aviso", "Telefone inválido! Use apenas números (10 ou 11 dígitos).")
                return

            if not novo_nome or not novo_telefone:
                messagebox.showwarning("Aviso", "Nome e telefone são obrigatórios!")
                return
            
            try:
                if self.conn:
                    cursor = self.conn.cursor()
                    
                    # Verifica se o telefone já existe (em outro cliente)
                    cursor.execute("SELECT id FROM clientes WHERE telefone = ? AND id != ?", 
                                  (novo_telefone, id_cliente))
                    if cursor.fetchone():
                        messagebox.showwarning("Aviso", "Telefone já cadastrado para outro cliente!")
                        return
                    
                    # Verifica se o email já existe (em outro cliente)
                    if novo_email:
                        cursor.execute("SELECT id FROM clientes WHERE email = ? AND id != ?", 
                                     (novo_email, id_cliente))
                        if cursor.fetchone():
                            messagebox.showwarning("Aviso", "Email já cadastrado para outro cliente!")
                            return

                    cursor.execute("""UPDATE clientes 
                                    SET nome = ?, email = ?, telefone = ? 
                                    WHERE id = ?""", 
                                 (novo_nome, novo_email, novo_telefone, id_cliente))
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                    janela_edicao.destroy()
                    self.carregar_clientes()
            except sqlite3.Error as err:
                messagebox.showerror("Erro SQLite", f"Falha ao atualizar:\n{err}")
        
        # Botão Salvar
        btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, width=15)
        btn_salvar.pack(pady=20)
    
    def limpar_campos(self):
        """Limpa os campos de entrada"""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
    
    def __del__(self):
        """Fecha a conexão com o banco de dados ao sair"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppClientesSimplificado(root)
    root.mainloop()
