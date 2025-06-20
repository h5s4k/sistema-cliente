```markdown
# Sistema Cliente

Projeto desenvolvido com o objetivo de aprofundar o conhecimento em **Python** e manipulação de **banco de dados**, explorando bibliotecas populares e boas práticas de estruturação de projetos.

## 📚 Objetivo

Este projeto foi criado como parte do meu aprendizado pessoal em:

- Criação de interfaces e funcionalidades com Python
- Manipulação de arquivos `.db` com bibliotecas específicas
- Empacotamento de aplicações com PyInstaller
- Organização de projetos em múltiplos diretórios

## ✨ Funcionalidades

- **Cadastro de clientes**: insere nome, e-mail e telefone no banco de dados.
- **Listagem automática**: exibe todos os clientes cadastrados ao iniciar o sistema.
- **Busca por nome**: filtra os clientes digitando parte do nome.
- **Edição de registros**: permite selecionar um cliente e atualizar seus dados.
- **Exclusão de clientes**: remove registros com confirmação.
- **Importação de dados via CSV**: permite carregar uma lista de clientes a partir de um arquivo `.csv`, facilitando a migração de dados.
- **Interface gráfica com Tkinter**: intuitiva, responsiva e fácil de usar.
- **Mensagens de feedback**: exibe alertas de sucesso ou erro com `messagebox`.
- **Banco de dados local (SQLite)**: persistência dos dados no arquivo `clientes.db`.
- **Executável independente (.exe)**: pode ser executado sem precisar abrir terminal ou instalar Python.
- **Compatível com Windows**: ideal para uso pessoal ou acadêmico em ambientes Windows.

## ⚙️ Tecnologias Utilizadas

- Python 3.x
- SQLite
- Tkinter
- PyInstaller
- VS Code (ambiente de desenvolvimento)
- Sistema operacional Windows

## 🚀 Como Executar

### ✅ Executar sem terminal

1. Acesse a pasta `dist/`
2. Localize o arquivo `sistemaBancoDeDados-2504023.exe`
3. Dê **duplo clique** no `.exe` para abrir o sistema de cadastro de clientes

> Não é necessário ter Python instalado para executar o `.exe`, desde que os arquivos gerados pelo PyInstaller estejam na mesma pasta.

### 💻 Executar via código-fonte

1. Clone o repositório:
   ```bash
   git clone https://github.com/h5s4k/sistema-cliente.git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd sistema-cliente
   ```
3. Execute o script principal:
   ```bash
   python sistemaBancoDeDados-2504023.py
   ```

## 📂 Estrutura do Projeto

- `sistemaBancoDeDados-2504023.py` – script principal da aplicação
- `clientes.db` – banco de dados local
- `build/` e `dist/` – pastas de empacotamento com PyInstaller
- `.spec` – configuração para gerar executável
- `.gitignore` – controle dos arquivos ignorados no Git
- `README.md` – este arquivo :)

## 🧠 Aprendizados

Durante o desenvolvimento deste projeto, aprofundei meus conhecimentos em:

- Manipulação de banco de dados SQLite via Python
- Organização de código e separação de responsabilidades
- Empacotamento de projetos Python para distribuição
- Leitura e importação de arquivos CSV com `pandas`
- Versionamento de código com Git e GitHub

## 📌 Nota

Este projeto tem fins **educacionais** e está em constante evolução à medida que avanços nos estudos são incorporados.

---

Feito com 💻 por **Francinaldo**
😄📁✨
´´´
