from wagtail.wagtailsnippets.models import register_snippet
from django.db import models
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer.
    Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in /templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return u"页面最底部文本 - 限单条"

    class Meta:
        verbose_name_plural = u'页面最底部文本'


@register_snippet
class Menu(models.Model):
    text = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = u'维基单页面左侧链接'
