# Generated by Django 3.0.5 on 2020-04-09 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='def.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
