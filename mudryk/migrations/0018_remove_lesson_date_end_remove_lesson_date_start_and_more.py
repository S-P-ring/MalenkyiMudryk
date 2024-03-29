# Generated by Django 4.2.7 on 2023-12-25 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mudryk', '0017_lesson_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='record',
            name='child_surname',
        ),
        migrations.RemoveField(
            model_name='record',
            name='parent_surname',
        ),
        migrations.AddField(
            model_name='course',
            name='max_members',
            field=models.PositiveIntegerField(default=10, verbose_name='Максимальна кількість учнів на занятті'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='datetime_start',
            field=models.DateTimeField(default='2023-12-25 17:37:00+02:00', verbose_name='Дата та час початку урока'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='email',
            field=models.EmailField(default='def@def.com', max_length=255, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Номер телефону повинен бути введений у такому форматі: 0639999999', regex='\\d{10}')], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='phone_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Номер телефону повинен бути введений у такому форматі: 0639999999', regex='\\d{10}')], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='current_participants',
            field=models.PositiveIntegerField(default=0, verbose_name='Поточна кількість учнів на це заняття'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='max_participants',
            field=models.PositiveIntegerField(verbose_name='Максимальна кількість учнів на занятті'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Назва курсу'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Номер телефону повинен бути введений у такому форматі: 0639999999', regex='\\d{10}')], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='record',
            name='child_name',
            field=models.CharField(max_length=255, verbose_name="Ім'я та прізвище дитини"),
        ),
        migrations.AlterField(
            model_name='record',
            name='parent_name',
            field=models.CharField(max_length=255, verbose_name="Ім'я та прізвище одного з батьків"),
        ),
    ]
