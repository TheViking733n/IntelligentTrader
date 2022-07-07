# Generated by Django 4.0.2 on 2023-06-21 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_ultimatecourse_ultimatecoursecustomer'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=13)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(default='', max_length=10)),
                ('address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
