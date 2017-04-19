from django.utils.html import format_html
# from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.wagtailcore import hooks


# @hooks.register('insert_global_admin_css')
@hooks.register('insert_editor_css')
def global_admin_css():
    # return format_html('<link rel="stylesheet" href="{}">', static('my/wagtail/theme.css'))
    return format_html('<link href="https://cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">')
