# Generated by Django 3.0.1 on 2020-06-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email address'),
        ),
    ]
