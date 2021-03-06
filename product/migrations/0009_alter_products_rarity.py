# Generated by Django 4.0.4 on 2022-05-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_products_rarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='rarity',
            field=models.CharField(choices=[('C', 'Common'), ('U', 'Uncommon'), ('R', 'Rare'), ('M', 'Mythic Rare'), ('L', 'Land')], default='C', max_length=20),
        ),
    ]
