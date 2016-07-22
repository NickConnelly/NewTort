from django import template

register = template.Library()

@register.inclusion_tag('sourcetextsformpage_form.html', takes_context=True)
def test_tag(context):
    # Look up the relevant form page by slug; replace FormPage and 'subscribe-now'
    # as appropriate for your site
    page = SourceTextsFormPage.objects.get(slug='new_source_text')
    return {
        'page': page,
        'form': page.get_form(),
        'request': context['request'],
    }
