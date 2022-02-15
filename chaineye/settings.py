import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '_f_iz-f@(*3cfgtq#kc2jfu@ynh=01ul9o#qr+6r49_7noimd)'


DEBUG = True
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "activity",
    'mdeditor',
    'DjangoUeditor',
    'common',
    'blogs',
    'webfront',
    "ceye_auth",
    "planet",
    "question",
    "wallet",
    "backoffice"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chaineye.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webfront.views.blog.global_variable',
            ],
        },
    },
]

WSGI_APPLICATION = 'chaineye.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chaineye',
        'USER': 'root',
        'PASSWORD': 'Wenwo2020!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

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

MDEDITOR_CONFIGS = {
    'default': {
        'width': '100% ',
        'height': 500,
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'zh'  # zh / en / es
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'format': '%(asctime)s %(name)s [%(module)s:%(levelname)s] %(message)s'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            # 'level':'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            # 'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
}

WALLET_URL = "http://60.205.1.144:8080/"

LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ACCESSKEYID = ''   # 短信验证吗 accessKeyId
ACCESSSECRET = ''  # 短信验证码 accessSecret
SIGNNAME = ''      # 短信验证码 SignName
TEMPLATECODE = ''  # 短信验证码 TemplateCode


try:
    from .local_settings import *
except ImportError:
    pass
