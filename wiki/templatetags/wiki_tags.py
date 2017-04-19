from django import template
from wiki.snippets import FooterText


register = template.Library()


@register.inclusion_tag('wiki/tags/footer.html', takes_context=True)
def wikihome_footer(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().body

    return {
        'footer_text': footer_text,
    }
