from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ProjectsApphook(CMSApp):
    name = _("Projects")
    urls = ["projects.urls"]
apphook_pool.register(ProjectsApphook)
