from django.db import models
from django.utils.html import format_html
from ckeditor_uploader.fields import RichTextUploadingField

class CourseSchedule2(models.Model):
    full = models.CharField(max_length = 32, verbose_name = 'Giorno e ora',)
    abbrev = models.CharField(max_length = 8, verbose_name = 'Abbreviazione',)

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = 'Orario'
        verbose_name_plural = 'Orari'

class Location(models.Model):
    title = models.CharField('Titolo',
        help_text='Il nome del luogo',
        max_length = 50)
    address = models.CharField('Indirizzo', max_length = 200,
        help_text = 'Via/Piazza, civico, CAP, Città',)
    gmap_link = models.URLField('Link di Google Map',
        blank= True, null=True,
        help_text="Dal menu di Google Maps seleziona 'Condividi/link', \
                   copia il link e incollalo qui",
    )
    gmap_embed = models.URLField('Incorpora Google Map',
        blank= True, null=True, max_length=500,
        help_text="Dal menu di Google Maps seleziona 'Condividi/incorpora', \
                   copia il link e incollalo qui",
    )
    body = RichTextUploadingField('Descrizione', )

    def get_gmap_link(self):
        link = format_html('<a href="{}" class="btn" target="_blank">Mappa</a>',
            self.gmap_link)
        return link
    get_gmap_link.short_description = 'Link di Google Maps'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Luogo'
        verbose_name_plural = 'Luoghi'
