# Generated by Django 2.2.7 on 2019-12-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_remove_lineitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
