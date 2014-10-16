#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    app = sys.argv[1]
    intervall = sys.argv[2]

    if intervall not in ["h", "d", "w"]:
        print("You need to set an intervall { h: hourly, d: daily, w: weekly }")
        exit(1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % app)

    from django.core.management import call_command

    from django.conf import settings

    if intervall == "d":
        call_command('clearsessions', interactive=False)

    if intervall == "h" and "haystack" in settings.INSTALLED_APPS:
        call_command('update_index', interactive=False, verbosity=0)
