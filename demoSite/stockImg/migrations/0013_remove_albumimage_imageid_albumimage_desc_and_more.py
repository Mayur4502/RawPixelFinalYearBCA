# Generated by Django 4.1.6 on 2023-03-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockImg', '0012_alter_img_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albumimage',
            name='imageid',
        ),
        migrations.AddField(
            model_name='albumimage',
            name='desc',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='albumimage',
            name='imageurl',
            field=models.ImageField(default='default.jpg', upload_to='media/images'),
        ),
    ]
