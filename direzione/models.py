from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import Member
from pagine.models import Location
from .choices import *

def user_directory_path(instance, filename):
    return 'conventions/{0}'.format(filename)

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

class Convention(models.Model):
    title = models.CharField('Nome', help_text="Il nome della convenzione",
        max_length = 50)
    slug = models.SlugField(max_length=50, unique=True, editable=False,
        null=True,)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Indirizzo',
        help_text="Inserire indirizzo e contatti" )
    description = models.TextField('Descrizione', blank= True, null=True,
        max_length = 500)

    def get_location(self):
        return self.location
    get_location.short_description = 'Sede'

    def get_path(self):
        return '/convenzioni/' + self.slug

    def save(self, *args, **kwargs):
        if not self.slug:  # create
            self.slug = generate_unique_slug(Convention, self.title)
        super(Convention, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Convenzione'
        verbose_name_plural = 'Convenzioni'

class ConventionUpload(models.Model):
    convention = models.ForeignKey(Convention, on_delete=models.CASCADE,
        related_name = 'convention_upload' )
    title = models.CharField('Nome', help_text="Il nome file",
        max_length = 50)
    upload = models.FileField('File',
        upload_to = user_directory_path,
        help_text="File da caricare",
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

class Society(models.Model):
    title = models.CharField('Nome', help_text="Il nome della società",
        max_length = 50)
    denomination = models.CharField('Denominazione', choices = DENOMINATION,
        max_length = 4)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
        null=True, verbose_name = 'Sede',
        help_text="Inserisce indirizzo e contatti" )
    coni = models.CharField('Registro CONI', blank= True, null=True,
        max_length = 10)
    fidal = models.CharField('Affiliazione FIDAL', blank= True, null=True,
        max_length = 10)
    fiscal_code = models.CharField('Codice Fiscale', blank= True, null=True,
        max_length = 11)
    iban = models.CharField('Codice IBAN', blank= True, null=True,
        max_length = 27)
    president = models.ForeignKey(Member, on_delete = models.SET_NULL,
        null=True, verbose_name = 'Presidente',
        related_name = 'society_president')
    executive = models.ManyToManyField(Member,
        verbose_name = 'Dirigenti', related_name = 'society_executive')
    trainers = models.ManyToManyField(Member,
        verbose_name = 'Istruttori', related_name = 'society_trainers')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Dati societari'
        verbose_name_plural = 'Dati societari'

class Institutional(models.Model):
    title = models.CharField('Titolo', max_length = 50)
    intro = models.CharField('Introduzione',
        blank= True, null=True, max_length = 100)
    body = RichTextUploadingField('Testo',
        help_text = "Scrivi qualcosa.", )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Pagina istituzionale'
        verbose_name_plural = 'Pagine istituzionali'
