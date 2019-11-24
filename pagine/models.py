import re
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug exists.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    Thanks to djangosnippets.org!
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

class CourseSchedule(models.Model):
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
    slug = models.SlugField(max_length=50, unique=True)
    address = models.CharField('Indirizzo', max_length = 200,
        help_text = 'Via/Piazza, civico, CAP, Città',)
    gmap_link = models.URLField('Link di Google Map',
        blank= True, null=True,
        help_text="Dal menu di Google Maps seleziona 'Condividi/link', \
                   copia il link e incollalo qui",
    )
    gmap_embed = models.TextField('Incorpora Google Map',
        blank= True, null=True, max_length=500,
        help_text="Dal menu di Google Maps seleziona 'Condividi/incorpora', \
                   copia il link e incollalo qui",
    )
    body = RichTextUploadingField('Descrizione', )

    def save(self, *args, **kwargs):
        if not self.gmap_embed.startswith('http'):
            # thanks to geeksforgeeks.com!
            list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.gmap_embed)
            if list:
                self.gmap_embed = list[0]
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Location, self.title)
        else:  # create
            self.slug = generate_unique_slug(Location, self.title)
        super(Location, self).save(*args, **kwargs)

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
