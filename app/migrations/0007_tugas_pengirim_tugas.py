# Generated by Django 4.1 on 2023-07-02 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_tugas_jenis'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugas',
            name='pengirim_tugas',
            field=models.ManyToManyField(blank=True, related_name='tugas_dikirim', to='app.userprofile'),
        ),
    ]
