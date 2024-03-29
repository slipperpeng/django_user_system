"""
Django settings for UserSystem project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import djcelery

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ew52rylz5aht)$ayirs1-#baf3)%pjrw7_)jv$u14^pqy^$2l9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userapp',
    'captcha',
    'restapp',
    'rest_framework.authtoken',
    'rest_framework',
    'djcelery'
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

ROOT_URLCONF = 'UserSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'UserSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

AUTH_USER_MODEL = "userapp.UserProfile"

# 配置发送激活链接的邮箱地址,账号密码等信息
EMAIL_HOST = "smtp.sina.cn"
EMAIL_PORT = 25
EMAIL_HOST_USER = "rjearlyup@sina.cn"
# cda3997346da4578)
EMAIL_HOST_PASSWORD = "cda39946da7814"
EMAIL_USE_TLS = False
EMAIL_FROM = "rjearlyup@sina.cn"

# 自定义backend记得来settings.py里面设置一下哇
AUTHENTICATION_BACKENDS = (
    'userapp.views.CustomBackend',

)

# —————————————分割线—————————————
# ———————————下面为restapp的设置——————————
# 上面的install_apps还要添加rest_framework.authtoken
# 缓存的设置,这里设置为使用本机缓存,还有其它的内存设置方式,如文件缓存,数据库缓存等
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

REST_FRAMEWORK = {
    # 1分钟内允许访问3次
    "DEFAULT_THROTTLE_RATES": {
        "xxx": "3/m"
    },
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    # 一页显示一条数据
    "page_size": 1
}

# —————————————分割线—————————————
# 实训的扩展（Celery）
# task 任务  worker 做任务的人 broker 任务队列  backend 做完任务的结果存储位置

djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/1'
# 设置worker的并发数量为2
CELERY_CONCURRENCY = 2
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
# 任务序列化和反序列化用json
CELERY_TASK_SERIALIZER = 'json'
# 结果序列化用json
CELERY_RESULT_SERIALIZER = 'json'

# 配置日志功能
ADMINS = [('slipper', '1160823499@qq.com'),]
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
LOGGING = {
    'version': 1,  # 指明版本
    'disable_existing_loggers': True,  # 禁用所有已经存在的日志配置
    # 配置格式器(IP地址、操作时间、行号、函数名、日志级别)
    'formatters': {
        # 详细
        'verbose': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        }
    },
    # 配置过滤器（debug为False才记录）
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    # 配置处理器（控制日志输出的位置）
    'handlers': {
        # 所有高于debug的信息都会被传到nullhander
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        # 配置邮件处理器,当出现ERROR时，会发送邮件至指定的邮箱
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 配置文件路径
            'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 最多5M
            'backupCount': 5,  # 最多有5个这种文件
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    # 定义记录器
    'loggers': {
        # 使用null处理器，所有高于（包括）info的消息会被发往null处理器，向父层次传递信息
        'django': {
            'handlers': ['file','console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        #所有高于（包括）error的消息会被发往mail_admins，debug处理器
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,  # 是否继承父类的log信息
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        }
    }
}

