# Generated by Django 4.2 on 2024-05-07 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('color_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('color_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('color_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('color_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('color_code', models.CharField(max_length=7)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gdrfad_api.course')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('color_code', models.CharField(max_length=7)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='gdrfad_api.service')),
            ],
        ),
    ]
