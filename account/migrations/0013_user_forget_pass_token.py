# Generated by Django 4.1.2 on 2022-11-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_rename_following_user_userfollowing_following_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='forget_pass_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]