# Generated by Django 4.1 on 2023-07-14 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tugas',
            name='jenis',
            field=models.CharField(choices=[('tugas', 'Tugas'), ('materi', 'Materi')], max_length=50),
        ),
    ]
