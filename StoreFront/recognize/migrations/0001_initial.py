# Generated by Django 3.2.8 on 2021-10-23 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='img')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='sellor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(default='', max_length=200, verbose_name='file_name')),
                ('name', models.CharField(max_length=20)),
                ('parentid', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='recognize.image', verbose_name='source')),
            ],
        ),
    ]
