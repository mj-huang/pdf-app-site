# Generated by Django 3.0.1 on 2020-06-16 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_ref_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ref_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref_2', to='users.Reference'),
        ),
        migrations.AddField(
            model_name='user',
            name='ref_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref_3', to='users.Reference'),
        ),
    ]