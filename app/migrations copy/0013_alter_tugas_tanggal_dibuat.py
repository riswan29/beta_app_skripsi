# Generated by Django 4.1 on 2023-06-29 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_tugas_tanggal_dibuat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tugas',
            name='tanggal_dibuat',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]