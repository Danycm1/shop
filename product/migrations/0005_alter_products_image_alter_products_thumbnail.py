# Generated by Django 4.0.4 on 2022-05-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_products_image_products_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cartes/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnail/'),
        ),
    ]
