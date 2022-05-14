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

#配置Redis为Django缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

ACCESSKEYID = 'LTAI4FsrVizgQCehFNZGBdJU'   # 短信验证吗 accessKeyId
ACCESSSECRET = 'prVvf6xYJoYTl99YZAlmbqBnZ6OaTG'  # 短信验证码 accessSecret
SIGNNAME = '问我学院'      # 短信验证码 SignName
TEMPLATECODE = 'SMS_183765549'  # 短信验证码 TemplateCode


