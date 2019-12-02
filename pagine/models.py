import os
import re
from PIL import Image
from datetime import datetime
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
#from ckeditor_uploader.fields import RichTextUploadingField

def date_directory_path(instance, filename):
    if instance.date:
        now = instance.date
    else:
        now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return 'uploads/{0}/{1}/{2}/{3}'.format(year, month, day, filename)

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

class ImageEntry(models.Model):
    name = models.CharField('Nome', editable=False, blank=True, null=True,
        max_length = 50,)
    date = models.DateTimeField(blank=True, null=True, editable=False)
    image = models.ImageField(upload_to = date_directory_path,)
    thumb = models.CharField(editable=False, blank=True, null=True,
        max_length = 200,)
    description = models.CharField('Descrizione', max_length = 200,
        blank=True, null=True,)

    def __str__(self):
        return self.name

    def get_thumb(self):
        thumb = format_html('<img src="{}" alt="{}" />', self.thumb,
            self.description)
        return thumb
    get_thumb.short_description = 'Anteprima'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
            super(ImageEntry, self).save(*args, **kwargs)
        if not self.name:
            self.name = 'IMG-' + self.date.strftime("%Y%m%d") + '-' + str(self.pk)
        url_extension = os.path.splitext(self.image.url)
        thumb_name = url_extension[0] + "_thumb" + url_extension[1]
        if not self.thumb == thumb_name:
            try:
                root_extension = os.path.splitext(self.image.path)
                size = (128, 128)
                img = Image.open(root_extension[0] + root_extension[1])
                img.thumbnail(size)
                img.save(root_extension[0] + "_thumb" + root_extension[1])
                self.thumb = thumb_name
            except:
                pass
        super(ImageEntry, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Immagine'
        verbose_name_plural = 'Immagini'

class Location(models.Model):
    image = models.ForeignKey(ImageEntry, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Immagine')
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
    body = models.TextField('Descrizione', blank= True, null=True,)

    def save(self, *args, **kwargs):
        if not self.gmap_embed.startswith('http'):
            # thanks to geeksforgeeks.com! findall returns a list
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
        if self.gmap_link:
            link = format_html('<a href="{}" class="btn" target="_blank">Mappa</a>',
                self.gmap_link)
        else:
            link = '-'
        return link
    get_gmap_link.short_description = 'Link di Google Maps'

    def get_thumb(self):
        if self.image:
            thumb = format_html('<img src="{}" alt="{}" />', self.image.thumb,
                self.image.description)
        else:
            thumb = ''
        return thumb
    get_thumb.short_description = 'Immagine'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Luogo'
        verbose_name_plural = 'Luoghi'
