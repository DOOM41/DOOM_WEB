from datetime import timedelta
from . import get_env_variable
from pathlib import Path
import os
import sys
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))


ADMIN_SITE_URL = get_env_variable("ADMIN_SITE_URL")

SECRET_KEY = get_env_variable("SECRET_KEY")

DEBUG = get_env_variable("DEBUG")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:8000',
]

binance_testnet_rpc_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.account.enable_unaudited_hdwallet_features()
MNEMONIC = get_env_variable("MNEMONIC")
ABI = get_env_variable("ABI")
my_contract_address = '0x817FEe66aECe8F7F79809ccD288B0e28e4500272'

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'deploy.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


AUTH_USER_MODEL = 'auths.CustomUser'


EMAIL_BACKEND = get_env_variable("EMAIL_BACKEND")
EMAIL_USE_TLS = get_env_variable("EMAIL_USE_TLS")
EMAIL_HOST = get_env_variable("EMAIL_HOST")
EMAIL_PORT = get_env_variable("EMAIL_PORT")
EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")

REST_FRAMEWORK: dict = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination',
    ),
    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
