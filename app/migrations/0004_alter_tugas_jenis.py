# Generated by Django 4.1 on 2023-07-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_jadwal_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tugas',
            name='jenis',
            field=models.CharField(choices=[('materi', 'Materi'), ('tugas', 'Tugas')], max_length=50),
        ),
    ]
