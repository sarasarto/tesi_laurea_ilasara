# Generated by Django 3.0.3 on 2020-03-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_studente'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='matricola',
            field=models.CharField(default=None, max_length=10),
        ),
    ]