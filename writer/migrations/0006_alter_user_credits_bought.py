# Generated by Django 3.2.4 on 2021-07-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writer', '0005_alter_user_credits_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='credits_bought',
            field=models.IntegerField(default=5),
        ),
    ]
