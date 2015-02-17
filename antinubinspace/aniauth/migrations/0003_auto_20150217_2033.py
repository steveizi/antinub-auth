# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import aniauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('aniauth', '0002_auto_20150217_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationkey',
            name='key_expiration',
            field=models.DateTimeField(default=aniauth.models.now_plus_two),
            preserve_default=True,
        ),
    ]
