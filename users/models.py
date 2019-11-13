from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import *

def user_directory_path(instance, filename):
    return 'user_uploads/{0}/{1}'.format(instance.user.username, filename)

class User(AbstractUser):

    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            try:
                memb = Member.objects.get(user_id = self.id)
                return
            except:
                memb = Member.objects.create(user = self, )
                memb.save()
                return
        else:
            children = Member.objects.filter(parent = self.id)
            if children:
                children.update(parent = None)

class CourseSchedule(models.Model):
    full = models.CharField(max_length = 32, verbose_name = 'Giorno e ora',)
    abbrev = models.CharField(max_length = 4, verbose_name = 'Abbreviazione',)

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = 'Orario'
        verbose_name_plural = 'Orari'

class Member(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO', verbose_name = 'Corre con noi?')
    parent = models.ForeignKey(User, on_delete = models.SET_NULL,
        blank = True, null = True, related_name = 'member_parent',
        verbose_name = 'Genitore')
    gender = models.CharField(max_length = 1, choices = GENDER,
        default = 'M', null=True, verbose_name = 'Sesso', )
    date_of_birth = models.DateField( blank=True, null=True,
        verbose_name = 'Data di nascita',)
    place_of_birth = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Luogo di nascita',)
    nationality = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Nazionalità',)
    fiscal_code = models.CharField(max_length = 16,
        blank = True, null = True, verbose_name = 'Codice fiscale',)
    address = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Indirizzo',
        help_text = 'Via/Piazza, civico, CAP, Città',)
    phone = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Telefono/i',)
    email_2 = models.EmailField(blank = True, null = True,
        verbose_name = 'Seconda email',)
    course = models.ManyToManyField('CourseSchedule',
        blank = True, verbose_name = 'Orari scelti', )
    course_alt = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Testo',
        help_text = "Se si è selezionato 'Altro'",)
    course_membership = models.CharField(max_length = 4, choices = COURSE,
        default = 'INTF', verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Compilare se si segue un corso',)
    no_course_membership = models.CharField(max_length = 4, choices = NO_COURSE,
        default = 'FID', verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Compilare se NON si segue un corso',)
    sign_up = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Richiesta di tesseramento',
        )
    privacy = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Privacy',
        )
    med_cert = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Certificato medico',
        )
    membership = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Tessera',)
    mc_expiry = models.DateField( blank=True, null=True,
        verbose_name = 'Scadenza CM/CMA',)
    mc_state = models.CharField(max_length = 4, choices = MC_STATE,
        verbose_name = 'Stato del CM/CMA',
        default = '0-NF',)
    settled = models.CharField(max_length = 4, choices = SETTLED,
        blank=True, null=True,
        verbose_name = 'In regola?',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def __str__(self):
        full_name = '%s %s' % (self.user.last_name, self.user.first_name)
        return full_name.strip()

    class Meta:
        verbose_name = 'Iscritto'
        verbose_name_plural = 'Iscritti'

class MemberPayment(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE,
        blank = True, null = True,related_name='member_payments')
    date = models.DateField( blank=True, null=True, verbose_name = 'Data')
    amount = models.FloatField( default = 0.00, verbose_name = 'Importo')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamenti'
