# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

from .umodels import RelatedLink
from .snippets import *
from .blocks import BaseStreamBlock

from datetime import datetime


# ------------------------主页-------------------------
class WikiHome(Page):
    logoname = models.CharField(
        max_length=255,
        help_text=u"显示在左上角的网页名称"
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=u"大幅背景图"
    )
    intro = models.TextField(
        blank=True,
        help_text=u"下方简单口号"
    )

    content_panels = Page.content_panels + [
        FieldPanel('logoname'),
        InlinePanel('toplinks', label="顶部右侧链接"),
        ImageChooserPanel('image'),
        FieldPanel('intro', classname="full"),
        InlinePanel('little_intros', label="下方一排推广简述"),
    ]


class WikiHomeTopLink(Orderable, RelatedLink):
    page = ParentalKey('wiki.WikiHome', related_name='toplinks')


class WikiHomeLittleIntros(Orderable):
    page = ParentalKey(WikiHome, related_name='little_intros')
    fa_name = models.CharField(blank=True, max_length=250,
                               help_text=u'''FontAwesome图标类名
                               - 参考fontawesome.io/icons/''')
    title = models.CharField(blank=True, max_length=250,
                             help_text=u"小标题")
    caption = models.CharField(blank=True, max_length=1000,
                               help_text=u"简述")

    panels = [
        FieldPanel('fa_name'),
        FieldPanel('title'),
        FieldPanel('caption'),
    ]


# ------------------------单维基页面-----------------------
class WikiPageTag(TaggedItemBase):
    content_object = ParentalKey('WikiPage', related_name='tagged_items')


class WikiPageTailLink(Orderable, RelatedLink):
    page = ParentalKey('WikiPage', related_name='related_links')


class WikiPage(Page):
    date = models.DateField(u"页面发布时间",
                            blank=True,
                            null=True,
                            default=datetime.now)
    tags = ClusterTaggableManager(through=WikiPageTag,
                                  blank=True,
                                  help_text=u"多个标签以空格符分隔")
    author = models.CharField(max_length=255,
                              help_text=u"作者，请添加自己的名字",
                              blank=True,
                              null=True)
    subtitle = models.CharField(max_length=255,
                                help_text=u"副标题",
                                blank=True,
                                null=True)
    body = StreamField(BaseStreamBlock(),
                       blank=True,
                       help_text=u"主内容",
                       verbose_name=u"页面主体")

    search_fields = Page.search_fields + [
        # index.SearchField('title'), # 不能有title，否则elasticsearch Map出错
        index.SearchField('subtitle'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('author'),
        ], heading=u"基本信息"),
        FieldPanel('subtitle', classname="full"),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label="底部相关链接"),
    ]

    @property
    def get_tags(self):
        tags = self.tags.all()
        prefix = WikiTagPage.objects.first().url + '?tag='
        # prefix = self.get_parent().url + '?tag='
        for tag, color in zip(tags, [
            '#5aba59', '#4d85d1', '#df2d4f', '#8156a7', '#999',
            '#5aba59', '#4d85d1', '#df2d4f', '#8156a7', '#999',
        ]):
            tag.url = prefix + tag.name
            tag.color = color
        return tags

    def get_context(self, request):
        '''
        添加左侧目录链接的上下文，以snippets形式注册并可在admin修改
        '''
        context = super(WikiPage, self).get_context(request)
        menus = Menu.objects.all()
        context['menus'] = menus
        return context

    parent_page_types = ['WikiHome', 'WikiTagPage']
    subpage_types = []


# --------------------------------标签页面--------------------------
class WikiTagPage(Page):

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag', None)
        if tag is None:
            tag = Tag.objects.first().name
            # redirect(WikiHome.objects.first().url)
        wikipages = WikiPage.objects.filter(tags__name=tag).live(
        ).order_by('-date')

        # Update template context
        context = super(WikiTagPage, self).get_context(request)
        context['tag'] = tag
        context['wikipages'] = wikipages
        # add bottom menus
        menus = Menu.objects.all()
        context['menus'] = menus
        return context

    @property
    def all_tags(self):
        tags = Tag.objects.all()
        prefix = self.url + '?tag='
        # prefix = self.get_parent().url + '?tag='
        for tag in tags:
            tag.url = prefix + tag.name
        return tags
