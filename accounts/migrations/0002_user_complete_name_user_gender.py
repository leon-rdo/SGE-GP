# Generated by Django 4.2.7 on 2023-11-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='complete_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome completo'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, null=True, verbose_name='Sexo'),
        ),
    ]
