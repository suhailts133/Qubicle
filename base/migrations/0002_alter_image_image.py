# Generated by Django 5.0 on 2024-03-08 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='uploaded_images/'),
        ),
    ]
