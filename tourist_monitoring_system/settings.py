
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sua_chave_secreta_aqui_E_MUITO_IMPORTANTE_ALTERAR_ISSO_EM_PRODUCAO' # Altere esta chave para uma string aleatória e segura em produção

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Mude para False em produção (desativa mensagens de erro detalhadas)

ALLOWED_HOSTS = [] # Lista de hosts/domínios permitidos para servir a aplicação (em branco para desenvolvimento)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', # Sistema de autenticação do Django
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages', # Sistema de mensagens (usado pelo admin e formulários)
    'django.contrib.staticfiles', # Gerenciamento de arquivos estáticos
    'tourism_app', # Seu aplicativo principal personalizado
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Proteção CSRF (importante para segurança)
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Habilita o sistema de autenticação
    'django.contrib.messages.middleware.MessageMiddleware', # Habilita o sistema de mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tourist_monitoring_system.urls' # O arquivo principal de URLs do projeto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Diretório onde Django procurará por templates globais
        'APP_DIRS': True, # Permite que o Django procure por templates dentro das pastas 'templates' de cada aplicativo
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', # Contexto para informações de usuário logado
                'django.contrib.messages.context_processors.messages', # Contexto para mensagens
            ],
        },
    },
]

WSGI_APPLICATION = 'tourist_monitoring_system.wsgi.application' # Ponto de entrada WSGI para servidores de produção


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'turismo', # Nome do seu banco de dados PostgreSQL
        'USER': 'turista', # Seu usuário do PostgreSQL
        'PASSWORD': 'brasil123', # Sua senha do PostgreSQL
        'HOST': 'localhost', # O host do seu servidor PostgreSQL (geralmente localhost)
        'PORT': '5432', # A porta do seu servidor PostgreSQL (padrão é 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br' # Define o idioma padrão da aplicação para português do Brasil

TIME_ZONE = 'America/Sao_Paulo' # Define o fuso horário para São Paulo, Brasil

USE_I18N = True # Habilita o sistema de internacionalização do Django

USE_L10N = True # Habilita a localização de dados (formato de números, datas, etc. específicos da região)

USE_TZ = True # Habilita o suporte a fusos horários no banco de dados e modelos


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/' # URL para servir arquivos estáticos

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Onde o Django buscará arquivos estáticos em desenvolvimento
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Onde os arquivos estáticos serão coletados em produção (para deploy)


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Tipo de campo padrão para chaves primárias automáticas

# Configurações de autenticação
LOGIN_REDIRECT_URL = 'dashboard' # Redireciona para a URL 'dashboard' após um login bem-sucedido
LOGOUT_REDIRECT_URL = 'login' # Redireciona para a URL 'login' após um logout bem-sucedido


