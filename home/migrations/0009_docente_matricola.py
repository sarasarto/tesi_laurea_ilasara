# Generated by Django 3.0.3 on 2020-03-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_docente_matricola'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='matricola',
            field=models.CharField(default='123', max_length=10),
        ),
    ]
