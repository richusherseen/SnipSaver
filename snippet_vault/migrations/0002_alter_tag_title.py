# Generated by Django 5.0.6 on 2024-05-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippet_vault', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]