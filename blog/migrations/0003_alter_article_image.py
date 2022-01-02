# Generated by Django 3.2.10 on 2021-12-29 01:23

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_translation_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='photos'),
        ),
    ]