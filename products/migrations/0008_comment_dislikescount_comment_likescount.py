# Generated by Django 4.1.2 on 2022-10-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikesCount',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='likesCount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
