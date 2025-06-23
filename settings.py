# tourist_monitoring_system/settings.py (Configura��es do Projeto Django)

import os

# Configura��es b�sicas do Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'sua_chave_secreta_aqui' # Altere esta chave para uma string aleat�ria e segura em produ��o
DEBUG = True # Mude para False em produ��o
ALLOWED_HOSTS = []


# Aplicativos instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tourism_app', # Seu aplicativo principal
]

# Middlewares para processar requisi��es e respostas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tourist_monitoring_system.urls' # O arquivo principal de URLs

# Configura��o de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Diret�rio para templates globais
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tourist_monitoring_system.wsgi.application' # Configura��o WSGI

# Configura��o do banco de dados (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_seu_banco', # Substitua pelo nome do seu banco de dados
        'USER': 'seu_usuario', # Substitua pelo seu usu�rio do PostgreSQL
        'PASSWORD': 'sua_senha', # Substitua pela sua senha do PostgreSQL
        'HOST': 'localhost', # Ou o IP/nome do host do seu banco de dados
        'PORT': '5432', # Porta padr�o do PostgreSQL
    }
}

# Valida��o de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionaliza��o
LANGUAGE_CODE = 'pt-br' # Linguagem em portugu�s do Brasil
TIME_ZONE = 'America/Sao_Paulo' # Fuso hor�rio
USE_I18N = True # Habilita internacionaliza��o
USE_L10N = True # Habilita localiza��o
USE_TZ = True # Habilita fusos hor�rios


# Arquivos est�ticos (CSS, JavaScript, Imagens)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Diret�rio para arquivos est�ticos globais
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Diret�rio onde os arquivos est�ticos ser�o coletados em produ��o


