from django import template

register = template.Library()


# settings value
@register.filter(name='frequencylistinput')
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page
