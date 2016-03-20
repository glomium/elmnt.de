if PROJECT_NAME and 'MEMCACHED_PORT_11211_TCP_ADDR' in os.environ:  # pragma: no cover
    CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
           'KEY_PREFIX': PROJECT_NAME,
           'LOCATION': '%s:%s' % (
                os.environ.get('MEMCACHED_PORT_11211_TCP_ADDR'),
                os.environ.get('MEMCACHED_PORT_11211_TCP_PORT', 11211),
           ),
        },
    }
    if not SESSION_ENGINE:
        SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
if not SESSION_ENGINE:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
