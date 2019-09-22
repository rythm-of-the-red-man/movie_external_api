# Generated by Django 2.2.5 on 2019-09-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20190919_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdbinfo',
            name='imdbid',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='imdbinfo',
            name='imdbrating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imdbinfo',
            name='imdbvotes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imdbinfo',
            name='metascore',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketinginfo',
            name='awards',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketinginfo',
            name='poster',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketinginfo',
            name='production',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='marketinginfo',
            name='rated',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='marketinginfo',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='country',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='plot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='type',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='source',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='actors',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='director',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='writer',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='dvd',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='released',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='year',
            field=models.DateField(blank=True, null=True),
        ),
    ]
