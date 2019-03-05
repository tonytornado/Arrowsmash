# Generated by Django 2.1.7 on 2019-03-05 03:05

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import Accounts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='default.jpg', upload_to=Accounts.models.user_directory_path)),
                ('rival_code', models.CharField(blank=True, max_length=9)),
                ('tagline',
                 models.CharField(blank=True, help_text="It's your life. What's its tag line?", max_length=100)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(
                    choices=[['NB', 'Non-Binary'], ['GQ', 'Gender-fluid'], ['M', 'Male'], ['F', 'Female'],
                             ['TM', 'Trans-Male'], ['TF', 'Trans-Female']], default='NB', help_text='We have to ask.',
                    max_length=2)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('bio', models.TextField(blank=True, max_length=5000)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='follow',
            name='followee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stalked',
                                    to='Accounts.Profile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stalker',
                                    to='Accounts.Profile'),
        ),
    ]
