from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TechnologyApphook(CMSApp):
    name = _("Projects")
    urls = ["technologies.urls"]
apphook_pool.register(TechnologyApphook)
