from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import TechnologyMenu


class TechnologyApphook(CMSApp):
    name = _("Technologies")
    urls = ["technologies.urls"]
    menus = [TechnologyMenu]
apphook_pool.register(TechnologyApphook)
