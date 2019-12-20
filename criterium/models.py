from datetime import datetime
from django.db import models

from users.models import User
from pagine.models import Event, Location, generate_unique_slug
from .choices import *

class Race(models.Model):
    title = models.CharField('Nome', help_text="Il nome della gara",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Evento')
    date = models.DateField('Data', blank= True, null=True,
        help_text="In mancanza di Evento", )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Luogo',
        help_text="In mancanza di Evento", )
    type = models.CharField('Tipo', choices = TYPE, max_length = 4,
        blank= True, null=True, )
    description = models.CharField('Descrizione', blank= True, null=True,
        max_length = 500)

    def get_date(self):
        if self.event:
            return self.event.date.date()
        return self.date
    get_date.short_description = 'Data'

    def get_location(self):
        if self.event:
            return self.event.location
        return self.location
    get_location.short_description = 'Luogo'

    def save(self, *args, **kwargs):
        if not self.slug:  # create
            self.slug = generate_unique_slug(Race, self.title)
        super(Race, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Gara'
        verbose_name_plural = 'Gare'
        ordering = ('-id', )

class Athlete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        verbose_name = 'Iscritto')
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
        editable = False, null = True, )
    points = models.IntegerField('Punti')
    placement = models.IntegerField('Piazzamento assoluto', blank = True,
        null = True, )
    time = models.TimeField('Tempo', blank = True, null = True, )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atleti/e'
        ordering = ('-id', )
