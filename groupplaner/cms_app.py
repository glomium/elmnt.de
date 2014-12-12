from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class GroupplanerApphook(CMSApp):
    name = _("Groupplaner")
    urls = ["groupplaner.urls"]
apphook_pool.register(GroupplanerApphook)
