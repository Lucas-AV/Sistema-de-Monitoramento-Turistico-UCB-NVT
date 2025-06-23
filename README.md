
# Sistema de Monitoramento Turístico - UCB-NVT

Repositório do projeto **'Sistema de Monitoramento Turístico'**, um projeto acadêmico desenvolvido para a disciplina de **Novas Tecnologias** da **Universidade Católica de Brasília (UCB)**.

Este sistema visa automatizar a coleta, visualização e análise de dados turísticos, oferecendo aos gestores um dashboard interativo com gráficos de visitação, relatórios detalhados com opções de exportação e um sistema de notificações para alertas de tendências.

**Tecnologias Utilizadas:** Python, Django, PostgreSQL, Plotly, Matplotlib e Tailwind CSS.

## Guia de Instalação e Execução

Este guia fornece as instruções passo a passo para configurar e executar o projeto **Sistema de Monitoramento Turístico** em seu ambiente local.

### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em seu sistema:

* **Python 3.11** (ou versão compatível com Django 5.x)

* **PostgreSQL** (Servidor de Banco de Dados)

* Um terminal de linha de comando (ex: PowerShell no Windows, Terminal no Linux/macOS)

### Configuração do Banco de Dados PostgreSQL

1.  **Instale o PostgreSQL:** Siga as instruções de instalação para o seu sistema operacional (consulte a documentação oficial do PostgreSQL). Durante a instalação, defina uma senha para o usuário padrão `postgres`.

2.  **Crie um Usuário e Banco de Dados para o Projeto:**
    Abra um terminal (`psql` ou ferramenta gráfica como pgAdmin) e conecte-se como o usuário `postgres`. Execute os seguintes comandos SQL, substituindo `turismo` pelo nome desejado para o banco de dados e `turista` e `brasil123` pelas suas credenciais:

    ```sql
    CREATE USER turista WITH PASSWORD 'brasil123' CREATEDB;
    CREATE DATABASE turismo OWNER turista;
    GRANT ALL PRIVILEGES ON DATABASE turismo TO turista;
    GRANT CREATE ON SCHEMA public TO turista;
    GRANT USAGE ON SCHEMA public TO turista;
    ALTER DEFAULT PRIVILEGES FOR ROLE turista IN SCHEMA public GRANT ALL ON TABLES TO turista;
    ALTER DEFAULT PRIVILEGES FOR ROLE turista IN SCHEMA public GRANT ALL ON SEQUENCES TO turista;
    ALTER DEFAULT PRIVILEGES FOR ROLE turista IN SCHEMA public GRANT ALL ON FUNCTIONS TO turista;
    ```

    *Obs: A permissão `CREATEDB` no usuário `turista` é opcional, mas útil para o Django criar o banco de dados se ele não existir.*

### Configuração do Projeto Django

1.  **Clone o Repositório:**
    No seu terminal, navegue até o diretório onde deseja armazenar o projeto e clone o repositório do GitHub:

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_GITHUB>
    cd tourist_monitoring_system
    ```

    *Substitua `<URL_DO_SEU_REPOSITORIO_GITHUB>` pela URL real do seu repositório.*

2.  **Crie e Ative o Ambiente Virtual:**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

    ```bash
    py -3.11 -m venv venv  # No Windows, usando Python 3.11
    # ou python3.11 -m venv venv # No Linux/macOS
    ```bash
    .\venv\Scripts\activate # No Windows
    # ou source venv/bin/activate # No Linux/macOS
    ```

    *O prompt do seu terminal deve mudar para indicar que o ambiente virtual está ativo (ex: `(venv) C:\...`).*

3.  **Instale as Dependências do Projeto:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt` (ou instale manualmente, se preferir):

    ```bash
    pip install Django psycopg2-binary matplotlib plotly pandas
    ```

4.  **Configure o `settings.py`:**
    Abra o arquivo `tourist_monitoring_system/settings.py` em seu editor de código. Certifique-se de que a seção `DATABASES` esteja configurada com as credenciais do PostgreSQL que você criou:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'turismo',
            'USER': 'turista',
            'PASSWORD': 'brasil123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

    *A `SECRET_KEY` deve ser alterada para um valor único e seguro em produção.*

5.  **Execute as Migrações do Banco de Dados:**
    Este comando criará as tabelas necessárias no seu banco de dados PostgreSQL.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crie um Superusuário (para acesso ao painel de administração):**
    Você precisará de um usuário para acessar o painel de administração do Django. Siga as instruções no terminal para definir um nome de usuário, e-mail e senha.

    ```bash
    python manage.py createsuperuser
    ```

## Executando o Projeto

1.  **Inicie o Servidor de Desenvolvimento:**
    No terminal, na pasta raiz do seu projeto e com o ambiente virtual ativo, execute:

    ```bash
    python manage.py runserver
    ```

    Você verá uma mensagem indicando que o servidor está rodando em um endereço como `http://127.0.0.1:8000/`.

2.  **Acesse a Aplicação:**
    Abra seu navegador e vá para `http://127.0.0.1:8000/`. Você será redirecionado para a página de login.

3.  **Acesse o Painel Administrativo (opcional):**
    Para gerenciar dados dos modelos, acesse `http://127.0.0.1:8000/admin/` e faça login com o superusuário que você criou.

Com esses passos, o projeto estará configurado e funcionando em sua máquina local.
