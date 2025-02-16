# Generated by Django 5.1.6 on 2025-02-15 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('farm', 'Farm'), ('organization', 'Organization')], default='individual', max_length=20),
        ),
    ]
