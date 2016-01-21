try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-pubuim').version
except Exception, e:
    VERSION = 'unknown'
