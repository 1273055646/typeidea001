# Generated by Django 3.2 on 2024-08-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_comment_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]
