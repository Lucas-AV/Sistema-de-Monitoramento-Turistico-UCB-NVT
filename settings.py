# tourist_monitoring_system/settings.py (Configurações do Projeto Django)

import os

# Configurações básicas do Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'sua_chave_secreta_aqui' # Altere esta chave para uma string aleatória e segura em produção
DEBUG = True # Mude para False em produção
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

# Middlewares para processar requisições e respostas
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

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Diretório para templates globais
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

WSGI_APPLICATION = 'tourist_monitoring_system.wsgi.application' # Configuração WSGI

# Configuração do banco de dados (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_seu_banco', # Substitua pelo nome do seu banco de dados
        'USER': 'seu_usuario', # Substitua pelo seu usuário do PostgreSQL
        'PASSWORD': 'sua_senha', # Substitua pela sua senha do PostgreSQL
        'HOST': 'localhost', # Ou o IP/nome do host do seu banco de dados
        'PORT': '5432', # Porta padrão do PostgreSQL
    }
}

# Validação de senha
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

# Internacionalização
LANGUAGE_CODE = 'pt-br' # Linguagem em português do Brasil
TIME_ZONE = 'America/Sao_Paulo' # Fuso horário
USE_I18N = True # Habilita internacionalização
USE_L10N = True # Habilita localização
USE_TZ = True # Habilita fusos horários


# Arquivos estáticos (CSS, JavaScript, Imagens)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Diretório para arquivos estáticos globais
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Diretório onde os arquivos estáticos serão coletados em produção


