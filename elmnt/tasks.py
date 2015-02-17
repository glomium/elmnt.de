#!/usr/bin/python
# ex:set fileencoding=utf-8:

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elmnt.settings")

from uwsgidecorators import cron
from django.core.management import call_command

from groupplaner.tasks import update as groupplaner_update

@cron(30, 0, -1, -1, -1)
def clearsesstions(num):
    call_command('clearsessions', interactive=False)
