from django.db import models

from users.models import User
from pagine.models import Event

class Race(models.Model):
    title = models.CharField('Nome', help_text="Il nome della gara",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Evento')
    date = models.DateField('Data', blank= True, null=True,
        help_text="In mancanza di Evento", )
    location = models.CharField('Luogo', blank= True, null=True,
        help_text="In mancanza di Evento", max_length = 50)
    description = models.CharField('Descrizione', blank= True, null=True,
        max_length = 500)

    def get_date(self):
        if self.event:
            return self.event.date
        return self.date

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Gara'
        verbose_name_plural = 'Gare'
        ordering = ('-id', )

# Create your models here.
