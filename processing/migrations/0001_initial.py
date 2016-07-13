# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fileUpload', models.FileField(upload_to=b'')),
                ('description', models.TextField(default=b'')),
                ('ext', models.CharField(max_length=7)),
                ('tipo', models.IntegerField(default=0, choices=[(0, b'output'), (1, b'input')])),
                ('tipo_multi', models.BooleanField(default=False)),
                ('test', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Archivos',
            },
        ),
        migrations.CreateModel(
            name='Fusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default=b'Image Fusion Multispectral and Pancromatic')),
                ('minAb', models.BigIntegerField()),
                ('maxAb', models.BigIntegerField()),
                ('out_file', models.ForeignKey(to='processing.File', null=True)),
            ],
            options={
                'verbose_name_plural': 'Procesos de alinear y estimar abundancia',
            },
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.IntegerField(default=3, choices=[(0, b'Terminado exitosamente'), (1, b'Terminado con errores'), (2, b'Ejecutandose'), (3, b'En espera')])),
                ('std_err', models.TextField(default=b'None')),
                ('std_out', models.TextField(default=b'None')),
                ('comando', models.CharField(default=b'echo Hola mundo', max_length=2000)),
                ('inicio', models.DateTimeField(auto_now_add=True)),
                ('fin', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Procesos',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.AddField(
            model_name='proceso',
            name='profile',
            field=models.ForeignKey(to='processing.Profile'),
        ),
        migrations.AddField(
            model_name='proceso',
            name='resultado',
            field=models.ForeignKey(blank=True, to='processing.File', null=True),
        ),
        migrations.AddField(
            model_name='fusion',
            name='procesos',
            field=models.ManyToManyField(to='processing.Proceso'),
        ),
        migrations.AddField(
            model_name='fusion',
            name='profile',
            field=models.ForeignKey(to='processing.Profile'),
        ),
        migrations.AddField(
            model_name='file',
            name='profile',
            field=models.ForeignKey(to='processing.Profile'),
        ),
    ]
