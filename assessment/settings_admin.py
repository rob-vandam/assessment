# this file is normally excluded in .gitignore
SECRET_KEY = 'django-insecure-aqz*4@q1#vvx1mqhal9l9ss@pcn5%0ffx-2tmld%^nn^h(36(q'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
        },
        'NAME': 'assessment',
        'USER': 'assessment',
        'PASSWORD': 'djdqcvmr@dskw1A',
        'HOST': '127.0.0.1',
        'PORT': '3306',

        'TEST': {
            'DEPENDENCIES': [],
            'NAME': 'test_assessment',
        },
    }
}