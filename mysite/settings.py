from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Hide development server warning
# https://docs.djangoproject.com/en/stable/ref/django-admin/#envvar-DJANGO_RUNSERVER_HIDE_WARNING
os.environ["DJANGO_RUNSERVER_HIDE_WARNING"] = "true"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gmq5ie-9v1hplg)p8))j(@u$)lrhm#-s7xnk-x8xqom!*pn+tj'

# SECURITY WARNING: don't run with debug turned on in production!
# Tắt DEBUG khi deploy để bảo mật
DEBUG = False

ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['infor-0cgw.onrender.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'testUrl',
    'api',
    'students',
    'profiles',
    'django_filters',
    'ajax',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        # Thêm SearchFilter của DRF vào đây để hỗ trợ LIKE
        'rest_framework.filters.SearchFilter',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Nếu có PostgreSQL thì dùng, không thì dùng SQLite
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Thêm đoạn này để kiểm tra xem Render có nhận được biến không
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Nơi chứa các file tĩnh gốc của bạn (nếu bạn để trong thư mục mysite/static)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Nơi Render sẽ gom file vào (nên đặt tên khác với STATICFILES_DIRS)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cấu hình WhiteNoise
if not DEBUG:
    # Trên Render (Production): Dùng WhiteNoise để nén và lưu cache mạnh
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # Trên Local: Dùng storage mặc định để tránh lỗi không tìm thấy file khi chưa chạy collectstatic
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_URL='/admin/'

# URL để chuyển hướng người dùng đến khi họ cố gắng truy cập một trang được bảo vệ (BẮT BUỘC)
LOGIN_URL = '/login/'

# URL để chuyển hướng người dùng đến sau khi đăng nhập thành công (Thường là trang Dashboard/Home)
LOGIN_REDIRECT_URL = '/test/temp/'  # Thay bằng URL của form bạn tạo

# URL để chuyển hướng người dùng đến sau khi đăng xuất
LOGOUT_REDIRECT_URL = '/test/home/'
