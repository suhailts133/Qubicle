# Generated by Django 5.0 on 2024-03-16 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_jsonfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSONModelQP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploaded_QP/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]