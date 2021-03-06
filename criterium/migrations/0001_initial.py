# Generated by Django 3.0.2 on 2020-01-26 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pagine', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Il nome della gara', max_length=50, verbose_name='Nome')),
                ('slug', models.SlugField(editable=False, null=True)),
                ('date', models.DateField(blank=True, help_text='In mancanza di Evento', null=True, verbose_name='Data')),
                ('type', models.CharField(blank=True, choices=[('P', 'Pista'), ('M', 'Maratona'), ('H', 'Mezza maratona'), ('C', 'Cross'), ('10', '10 mila')], max_length=4, null=True, verbose_name='Tipo')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descrizione')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_race', to='pagine.Event', verbose_name='Evento')),
                ('location', models.ForeignKey(blank=True, help_text='In mancanza di Evento', null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.Location', verbose_name='Luogo')),
            ],
            options={
                'verbose_name': 'Gara',
                'verbose_name_plural': 'Gare',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='Punti')),
                ('placement', models.IntegerField(blank=True, null=True, verbose_name='Piazzamento assoluto')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Tempo')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Member', verbose_name='Iscritto')),
                ('race', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='criterium.Race')),
            ],
            options={
                'verbose_name': 'Atleta',
                'verbose_name_plural': 'Atleti/e',
                'ordering': ('-id',),
            },
        ),
    ]
