#!/usr/bin/python
# ex:set fileencoding=utf-8:

try:
    import uwsgi
except ImportError:
    uwsgi = None

from cms.signals import urls_need_reloading

def server_restart(**kwargs):
    print "SERVER RELOAD!!!"
    if uwsgi is not None and uwsgi.masterpid() > 0:
        uwsgi.reload()

urls_need_reloading.connect(server_restart)
