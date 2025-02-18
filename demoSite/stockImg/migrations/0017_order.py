# Generated by Django 4.1.6 on 2023-04-06 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockImg', '0016_remove_albumimage_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('OrderDateTime', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(default=0)),
                ('imageid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stockImg.img')),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stockImg.user')),
            ],
        ),
    ]
