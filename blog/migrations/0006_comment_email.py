# Generated by Django 3.0.4 on 2020-07-05 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='exit', max_length=254),
            preserve_default=False,
        ),
    ]
