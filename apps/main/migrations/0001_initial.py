# Generated by Django 5.1.7 on 2025-03-15 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('title', models.CharField(help_text='Professional title or role', max_length=200)),
                ('summary', models.TextField(help_text='Brief professional summary')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'CV',
                'verbose_name_plural': 'CVs',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone'), ('linkedin', 'LinkedIn'), ('github', 'GitHub'), ('website', 'Website')], max_length=50)),
                ('value', models.CharField(max_length=255)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.cv')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('technologies', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='main.cv')),
            ],
        ),
        migrations.CreateModel(
            name='CVSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], max_length=50)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='main.cv')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cvs', to='main.skill')),
            ],
        ),
    ]
