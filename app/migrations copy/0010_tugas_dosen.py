# Generated by Django 4.1 on 2023-06-29 15:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_tugas_jurusan_tugas_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugas',
            name='dosen',
            field=models.ForeignKey(default=datetime.datetime(2023, 6, 29, 15, 6, 11, 993464, tzinfo=datetime.timezone.utc), limit_choices_to={'role': 'dosen'}, on_delete=django.db.models.deletion.CASCADE, to='app.userprofile'),
            preserve_default=False,
        ),
    ]
