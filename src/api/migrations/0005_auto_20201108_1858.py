# Generated by Django 3.1.3 on 2020-11-08 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201108_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketclaimmapping',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='ticketclaimmapping',
            old_name='employer_id',
            new_name='employer',
        ),
    ]
