# Generated by Django 4.1 on 2023-06-24 08:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_jadwal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_tugas', models.CharField(max_length=100)),
                ('tanggal_dibuat', models.DateTimeField(default=datetime.datetime.now)),
                ('deadline', models.DateTimeField()),
                ('keterangan', models.TextField(blank=True)),
                ('file_tugas', models.FileField(upload_to='tugas_files/')),
            ],
        ),
        migrations.AlterField(
            model_name='jadwal',
            name='dosen',
            field=models.ForeignKey(limit_choices_to={'role': 'dosen'}, on_delete=django.db.models.deletion.CASCADE, to='app.userprofile'),
        ),
    ]
