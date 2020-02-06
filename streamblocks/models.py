from django.db import models
from django.utils.text import slugify
from filebrowser.fields import FileBrowseField

class IndexedParagraph(models.Model):
    title = models.CharField(max_length = 100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    def get_slug(self):
        return slugify( self.title )

    class Meta:
        verbose_name="Paragrafo indicizzato"
        verbose_name_plural="Paragrafi indicizzati"

class CaptionedImage(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png"], null=True, blank=True)
    caption = models.CharField(max_length = 200, blank=True, null=True)

    class Meta:
        verbose_name="Immagine con didascalia"
        verbose_name_plural="Immagini con didascalia"

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    IndexedParagraph,
    CaptionedImage,
]
