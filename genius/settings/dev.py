from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y*lzg&g@lvz)fufwce&ul2t$gnrtcusce47n8tr*vyrg*o!=0&'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# http://docs.wagtail.io/en/v1.9/topics/search/backends.html#wagtailsearch-backends-elasticsearch
# https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-smartcn.html#analysis-smartcn-tokenizer
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch5',
        'URLS': ['http://localhost:9200'],
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {
            'settings': {
                'index': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0,
                    'analysis': {
                        'analyzer': {
                            'default': {
                                'type': 'smartcn'
                                # 可以使用smartcn
                            }
                        }
                    }
                }
            }
        }
    }
}

ALLOWED_HOSTS = ['*',]

try:
    from .local import *
except ImportError:
    pass
