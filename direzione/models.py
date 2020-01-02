from django.db import models
from django.utils.text import slugify
from pagine.models import Location

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
