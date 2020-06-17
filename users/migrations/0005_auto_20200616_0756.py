# Generated by Django 3.0.1 on 2020-06-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_reference_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reference',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reference',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Name'),
        ),
    ]
