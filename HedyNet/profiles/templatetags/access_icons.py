from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from profiles import constants

register = template.Library()

@register.filter
@stringfilter
def access_label(value):
    """Converts an access value into a label with icon."""
    
    icon = access_icon(value)
    
    if icon:
        return mark_safe('%s %s' % (value, icon))
    
    # Just the value if no icon
    return value
    
@register.filter
@stringfilter
def access_icon(value):
    """Converts an access value into an icon."""
    
    if value == constants.PUBLIC_ACCESS:
        return mark_safe('<i class="fa fa-unlock-alt"></i>')
    if value == constants.REGISTERED_ACCESS:
        return mark_safe('<i class="fa fa-unlock"></i>')
    if value == constants.MEMBERS_ACCESS:
        return mark_safe('<i class="fa fa-lock"></i>')
    if value in (constants.PRIVATE_ACCESS, constants.ADMIN_ACCESS):
        return mark_safe('<i class="fa fa-eye"></i>')
    
    return ''
