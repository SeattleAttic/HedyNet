from __future__ import unicode_literals

from django.utils.safestring import mark_safe
from django.template import Template, Context

import markdown_deux

def render_template_markdown(content, markdown_settings=None, context=Context()):

    tt=Template(content)
    template_content = tt.render(context)
    html_content = markdown_deux.markdown(template_content, markdown_settings)
    return mark_safe(html_content)
