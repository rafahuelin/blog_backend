# Generated by Django 3.2.10 on 2022-01-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tagtranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagtranslation',
            name='translation',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
