from django.db import models

class CourseSchedule2(models.Model):
    full = models.CharField(max_length = 32, verbose_name = 'Giorno e ora',)
    abbrev = models.CharField(max_length = 8, verbose_name = 'Abbreviazione',)

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = 'Orario'
        verbose_name_plural = 'Orari'
