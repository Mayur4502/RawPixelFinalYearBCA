# Generated by Django 4.1.6 on 2023-03-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockImg', '0005_album_catagory_img_tags_save_like_comment_albumimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='url',
            field=models.ImageField(upload_to='media/images'),
        ),
    ]
