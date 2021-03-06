# Generated by Django 2.2.1 on 2019-05-06 13:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_version', models.CharField(max_length=20)),
                ('page_title', models.CharField(max_length=100)),
                ('internal_links', models.IntegerField()),
                ('external_links', models.IntegerField()),
                ('inaccessible_links', models.IntegerField()),
                ('has_loginform', models.BooleanField()),
                ('delete_on', models.DateTimeField(default=datetime.datetime(2019, 5, 7, 14, 35, 56, 510738))),
            ],
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('H1', 'Heading Type 1'), ('H2', 'Heading Type 2'), ('H3', 'Heading Type 3'), ('H4', 'Heading Type 4'), ('H5', 'Heading Type 5'), ('H6', 'Heading Type 6')], max_length=2)),
                ('count', models.IntegerField()),
                ('webpage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AnalysisApplication.WebPage')),
            ],
        ),
    ]
