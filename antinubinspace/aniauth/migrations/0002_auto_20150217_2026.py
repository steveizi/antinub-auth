# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aniauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationkey',
            name='key_expiration',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 19, 20, 26, 38, 165000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
