# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaytmHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('ORDERID', models.CharField(max_length=30, verbose_name='ORDER ID')),
                ('TXNDATE', models.DateTimeField(default=django.utils.timezone.now, verbose_name='TXN DATE')),
                ('TXNID', models.IntegerField(verbose_name='TXN ID')),
                ('BANKTXNID', models.IntegerField(null=True, blank=True, verbose_name='BANK TXN ID')),
                ('BANKNAME', models.CharField(null=True, blank=True, max_length=50, verbose_name='BANK NAME')),
                ('RESPCODE', models.IntegerField(verbose_name='RESP CODE')),
                ('PAYMENTMODE', models.CharField(null=True, blank=True, max_length=10, verbose_name='PAYMENT MODE')),
                ('CURRENCY', models.CharField(null=True, blank=True, max_length=4, verbose_name='CURRENCY')),
                ('GATEWAYNAME', models.CharField(null=True, blank=True, max_length=30, verbose_name='GATEWAY NAME')),
                ('MID', models.CharField(max_length=40)),
                ('RESPMSG', models.TextField(max_length=250, verbose_name='RESP MSG')),
                ('TXNAMOUNT', models.FloatField(verbose_name='TXN AMOUNT')),
                ('STATUS', models.CharField(max_length=12, verbose_name='STATUS')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='rel_payment_paytm')),
            ],
        ),
    ]
