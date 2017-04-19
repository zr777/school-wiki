from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock,
    StreamBlock, StructBlock, TextBlock, RawHTMLBlock,
)
from wagtail.contrib.table_block.blocks import TableBlock
# icons can be seen in http://localhost:8000/admin/styleguide/


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select
    h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('h4', 'H4'),
        ('h3', 'H3'),
        ('h2', 'H2'),
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute
    a quote to the author
    """
    text = TextBlock(label=u'文本')
    attribute_name = CharBlock(
        blank=True, required=False, label=u'署名')

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock(label="标题", heading_text="请选择字号")
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        label=u"段落"
    )
    image_block = ImageBlock(label=u"图片", icon="image")
    block_quote = BlockQuote(label=u"引用", )
    table_block = TableBlock(label=u"表格",)
    raw_html = RawHTMLBlock(icon="code", label='Raw HTML')
    # document = DocumentChooserBlock(icon="doc-full-inverse")
