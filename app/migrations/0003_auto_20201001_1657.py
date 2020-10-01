# Generated by Django 3.1.1 on 2020-10-01 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20201001_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='val',
            field=models.JSONField(default=[{'image': '123', 'title': 'abc'}]),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='category',
            field=models.CharField(blank=True, default='', max_length=100, null=''),
        ),
    ]