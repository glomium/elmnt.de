from django.utils.translation import ugettext_lazy as _

from pygments import highlight
from pygments import styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import PygmentsPlugin

class CMSPygmentsPlugin(CMSPluginBase):
    model = PygmentsPlugin
    name = _("Pygments")
    render_template = "cmspygments/pygments.html"
    parent_classes = ['ColumnPlugin', 'SectionPlugin', 'MediaObjectPlugin', 'TextPlugin']
    allow_children = False
    
    def render(self, context, instance, placeholder):
        style = styles.get_style_by_name("default")
        formatter = HtmlFormatter(linenos=instance.linenumbers, style=style)
        lexer = get_lexer_by_name(instance.code_language)
        context.update({
            'pygments_html': highlight(instance.code, lexer, formatter),
            'css': formatter.get_style_defs(),
            'object':instance,
            'placeholder':placeholder,
        })
        return context

plugin_pool.register_plugin(CMSPygmentsPlugin)
