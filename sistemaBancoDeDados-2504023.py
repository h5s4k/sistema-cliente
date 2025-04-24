import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys

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
        
        # Treeview para exibir clientes
        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Nome", "Email", "Telefone"), show="headings")
        
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
        
        # Botão Excluir
        btn_excluir = tk.Button(frame_botoes, text="Excluir", command=self.excluir_cliente, width=15)
        btn_excluir.pack(side="left", padx=5)
        
        # Botão Editar
        btn_editar = tk.Button(frame_botoes, text="Editar", command=self.editar_cliente, width=15)
        btn_editar.pack(side="left", padx=5)
    
    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        
        # Validação dos campos
        if not nome or not email or not telefone:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            if self.conn:
                cursor = self.conn.cursor()
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
    
    def excluir_cliente(self):
        """Exclui o cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return
        
        id_cliente = self.tree.item(selecionado)["values"][0]
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?"):
            try:
                if self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    self.carregar_clientes()
            except sqlite3.Error as err:
                messagebox.showerror("Erro SQLite", f"Falha ao excluir:\n{err}")
    
    def editar_cliente(self):
        """Edita o cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        # Obtém os dados atuais
        item = self.tree.item(selecionado)
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
            
            if not novo_nome or not novo_email or not novo_telefone:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            try:
                if self.conn:
                    cursor = self.conn.cursor()
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
    