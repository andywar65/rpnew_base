from django.db import models
from django.utils.text import slugify
from filebrowser.fields import FileBrowseField
from .choices import *

class IndexedParagraph(models.Model):
    height = models.CharField('Altezza titolo', max_length=1, choices = HEIGHT,
        default='4')
    title = models.CharField('Titolo', max_length = 100, blank=True, null=True)
    body = models.TextField('Testo', blank=True, null=True,
        help_text="Accetta tag HTML")

    def get_slug(self):
        return slugify( self.title )

    class Meta:
        verbose_name="Paragrafo indicizzato"
        verbose_name_plural="Paragrafi indicizzati"

class CaptionedImage(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png"], null=True, blank=True)
    caption = models.CharField("Didascalia", max_length = 200, blank=True,
        null=True)

    class Meta:
        verbose_name="Immagine con didascalia"
        verbose_name_plural="Immagini con didascalia"

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    IndexedParagraph,
    CaptionedImage,
]
