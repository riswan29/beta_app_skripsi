# Generated by Django 4.1 on 2023-06-29 15:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugas',
            name='nama_pengguna',
            field=models.CharField(default=django.utils.timezone.now, editable=False, max_length=100),
            preserve_default=False,
        ),
    ]
