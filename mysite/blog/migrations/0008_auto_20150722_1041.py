# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20150714_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'default_permissions': ()},
        ),
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 22, 8, 41, 10, 255151, tzinfo=utc)),
        ),
    ]
