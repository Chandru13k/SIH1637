# Generated by Django 5.1.6 on 2025-03-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_farmprofile_farmlocation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmprofile',
            name='heroImg',
            field=models.ImageField(null=True, upload_to='hero/IMG/'),
        ),
        migrations.AlterField(
            model_name='farmprofile',
            name='profileImg',
            field=models.ImageField(null=True, upload_to='profile/IMG/'),
        ),
        migrations.AlterField(
            model_name='individualprofile',
            name='heroImg',
            field=models.ImageField(null=True, upload_to='hero/IMG/'),
        ),
        migrations.AlterField(
            model_name='individualprofile',
            name='profileImg',
            field=models.ImageField(null=True, upload_to='profile/IMG/'),
        ),
        migrations.AlterField(
            model_name='organizationprofile',
            name='heroImg',
            field=models.ImageField(null=True, upload_to='hero/IMG/'),
        ),
        migrations.AlterField(
            model_name='organizationprofile',
            name='profileImg',
            field=models.ImageField(null=True, upload_to='profile/IMG/'),
        ),
    ]
