# Generated by Django 4.1 on 2022-11-15 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('catchphrase', models.TextField(blank=True, null=True)),
                ('picture_0', models.ImageField(upload_to='mainimages')),
                ('picture_1', models.ImageField(blank=True, null=True, upload_to='./product/static/product/imgs')),
                ('picture_2', models.ImageField(blank=True, null=True, upload_to='./product/static/product/imgs')),
                ('short_term_price', models.IntegerField(default=0)),
                ('long_term_price', models.IntegerField(default=0)),
                ('tax', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.listing')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.tag'),
        ),
    ]
