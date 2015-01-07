from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class WeightsApphook(CMSApp):
    name = _("Weights")
    urls = ["weights.urls"]
apphook_pool.register(WeightsApphook)
