# Generated by Django 4.0.1 on 2024-03-20 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=None, upload_to='blogimage'),
        ),
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]