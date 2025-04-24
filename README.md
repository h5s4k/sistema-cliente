Resumo do Projeto: Sistema de Gerenciamento de Clientes
Francinaldo de Castro Silva

🎯 Objetivo
Uma aplicação simples para desktop de cadastro e gestão de clientes, com armazenamento local e interface intuitiva, utilizando:
- Python (linguagem principal)
- Tkinter (interface gráfica)
- SQLite (banco de dados embutido)
- PyInstaller (empacotamento como executável)

🔧 Funcionalidades Principais
1. CRUD Completo
   - Create: Cadastro de novos clientes (nome, e-mail, telefone)
   - Read: Listagem em tabela interativa (Treeview)
   - Update: Edição de registros existentes
   - Delete: Exclusão com confirmação

2. Persistência de Dados
   - Armazenamento automático em banco de dados SQLite (`clientes.db`)
   - Criação automática da tabela se não existir

3. Interface Amigável
   - Janelas de diálogo para edição
   - Validação de campos obrigatórios

4. Distribuição
   - Conversão para executável (.exe) com ícone personalizado

⚙️ Tecnologias e Bibliotecas
| Componente        | Finalidade                          |  
|-------------------|-------------------------------------|  
| tkinter           | Interface gráfica                   |  
| sqlite3           | Armazenamento local                 |  
| pyinstaller       | Criação do executável               |  
| messagebox        | Exibição de alertas e confirmações  |  


📂 Estrutura do Código
código python

class AppClientesSimplificado:
    def __init__(self):
        # Configura janela principal
        # Conexão com SQLite
        # Cria widgets (campos de texto, botões, tabela)

    def cadastrar_cliente(self):
        # Valida e insere dados no banco

    def carregar_clientes(self):
        # Preenche a tabela com registros do banco

    def editar_cliente(self):
        # Abre janela de edição e salva alterações

    def excluir_cliente(self):
        # Remove registro com confirmação


🚀 Como Executar
1. Requisitos: Python 3.8+
2. Instalação:
   bash
   pip install pyinstaller
   
3. Execução:
   bash
   python app_clientes.py
   
4. Compilar para .exe:
   bash
   pyinstaller --onefile --windowed --icon=icone.ico app_clientes.py


Resumo do Código: Sistema de Clientes

Estrutura Principal
código python

class AppClientesSimplificado:
    def __init__(self, root):
        # 1. Configura janela principal (Tkinter)
        # 2. Conecta ao SQLite (clientes.db)
        # 3. Cria interface:
        #    - Campos: nome, email, telefone
        #    - Treeview (tabela)
        #    - Botões: Cadastrar/Editar/Excluir

Métodos Essenciais

| Método             | Funcionalidade                                                        |
|--------------------|-----------------------------------------------------------------------|
|conectar_banco()    | Estabelece conexão com o SQLite (cria `clientes.db` se não existir)   |
|criar_tabela()      | Cria tabela `clientes` (id, nome, email, telefone)                    |
|cadastrar_cliente() | Valida campos → insere no banco → atualiza tabela                     |
|carregar_clientes() | Busca registros no SQLite → exibe na Treeview                         |
|editar_cliente()    | Abre popup de edição → salva alterações no banco                      |
|excluir_cliente()   | Remove registro com confirmação (messagebox)                          |
|limpar_campos()     | Reseta os campos de entrada                                           |


Fluxo de Dados
1. Entrada
   - Usuário preenche campos (nome/email/telefone)
   - Validação: `if not nome or not email...`

2. Processamento
   - Operações SQL:
     código python

     cursor.execute("INSERT INTO clientes VALUES (?, ?, ?)", (nome, email, telefone))

3. Saída
   - Atualização automática da Treeview
   - Feedback visual (messagebox de sucesso/erro)


Destaques Técnicos
-Tratamento de Erros:
  código python

  try:
      cursor.execute(...)
  except sqlite3.Error as err:
      messagebox.showerror("Erro SQLite", f"Falha: {err}")

-Gerenciamento de Recursos:
  código python

  def __del__(self):
      if self.conn:
          self.conn.close()  # Fecha conexão ao sair

-Path Dinâmico:
  código python

  if getattr(sys, 'frozen', False):
      application_path = os.path.dirname(sys.executable)  # Para .exe


Extensibilidade
- Facilmente modificável para adicionar:
  - Novos campos (ex: endereço)
  - Filtros por nome/email
  - Exportação para CSV

Código completo: [GitHub](https://github.com/h5s4k/sistema-cliente)
   
